from typing import Any, Dict, List, Optional, Type

from sqlalchemy import and_, any_, select
from sqlalchemy.sql.expression import BinaryExpression, ColumnClause
from xcnt.sqlalchemy.search import (
    EvaluationErrorCode,
    EvaluationResult,
    FieldParser,
    FieldPlugin,
    FilterFieldParser,
    fields,
)
from xcnt.sqlalchemy.search.fields.scalar.base_scalar import BaseScalarField
from xcnt.sqlalchemy.search.parser.flow_exception import ReturnAll
from xcnt.sqlalchemy.search.parser.nested_query import NestedQueryParser

from xcnt.drivr.metadata_client.model import (
    INITIATED_METADATA_VALUE_CLASSES,
    INITIATED_METADATA_VALUE_LOOKUP_CLASSES,
    MetadataType,
    MetadataValue,
    MetadataValueLookup,
)
from xcnt.drivr.metadata_client.model.metadata_value import _metadata_type_class_for
from xcnt.drivr.metadata_client.search.metadata_item import MetadataItem
from xcnt.drivr.metadata_client.search.metadata_key_value_store_field import (
    MetadataGenericValueField,
    MetadataKeyValueStoreField,
)
from xcnt.drivr.metadata_client.search.metadata_type_key import MetadataTypeKey
from xcnt.drivr.metadata_client.search.parser.metadata_base_lookup_parser_mixin import MetadataBaseLookupParserMixin


class MetadataTypeKeyParser(FilterFieldParser[MetadataTypeKey]):
    @classmethod
    def supports(self, entity: fields.BaseField) -> bool:
        return isinstance(entity, MetadataTypeKey)

    @property
    def metadata_type_class(self) -> Type[MetadataTypeKey]:
        return self.resource_field.metadata_type_class

    @property
    def model_field(self) -> ColumnClause:
        return self.metadata_type_class.key

    @property
    def model(self) -> Type[MetadataType]:
        return self.metadata_type_class

    @property
    def mapping_field(self) -> BaseScalarField:
        return fields.Sha256String()


class MetadataKeyValueStoreFieldParser(
    FieldPlugin[MetadataKeyValueStoreField, Dict[str, Any]], MetadataBaseLookupParserMixin
):
    @classmethod
    def supports(self, entity: fields.BaseField) -> bool:
        return isinstance(entity, MetadataKeyValueStoreField)

    @property
    def entity_type(self) -> str:
        return self.resource_field.entity_type

    @property
    def _metadata_value_class(self) -> Type[MetadataValue]:
        return INITIATED_METADATA_VALUE_CLASSES[self.entity_type]

    @property
    def _metadata_value_lookup_class(self) -> Type[MetadataValueLookup]:
        return INITIATED_METADATA_VALUE_LOOKUP_CLASSES[self.entity_type]

    @property
    def _metadata_type_class(self) -> Type[MetadataType]:
        return _metadata_type_class_for(self._metadata_value_lookup_class.metadata_type)

    def parse(self, parse_context: Dict[str, Any]) -> EvaluationResult:
        self.parse_context = parse_context
        expressions = []

        for key, value in self.query.items():
            expression = None
            if key == "key":
                expression = self._parse_key_field(value)
            elif key == "value":
                expression = self._parse_value_field(value)
            else:
                self.errors[key] = EvaluationErrorCode.UNKNOWN_FIELD
            expressions.append(expression)

        if len(expressions):
            expression = and_(*expressions)
            if (domain_uuid := self.domain_uuid) is not None:
                expression = and_(expression, self._metadata_type_class.domain_uuid == domain_uuid)

            self.expressions.append(
                self.model_primary_key
                == any_(
                    select([self._metadata_value_lookup_class.entity_uuid])
                    .join(
                        self._metadata_value_class,
                        self._metadata_value_lookup_class.metadata_value_uuid == self._metadata_value_class.uuid,
                        isouter=True,
                    )
                    .where(expression)
                    .scalar_subquery()
                )
            )
        else:
            raise ReturnAll()

        return self._result_from_state()

    def _parse_key_field(self, field_data: Any) -> Optional[BinaryExpression]:
        key_field = MetadataTypeKey(self._metadata_type_class)
        key_field.resource = self.resource_field.resource

        field_parser = FieldParser("key", field_data, key_field)
        try:
            evaluation_result = field_parser.parse(self.parse_context)
        except ReturnAll:
            return []

        clause = evaluation_result.build_clauses()
        if clause is not None:
            clause = and_(
                clause, self._metadata_value_lookup_class.metadata_type_uuid == self._metadata_type_class.uuid
            )
        return clause

    def _parse_value_field(self, field_data: Any) -> Optional[BinaryExpression]:
        value_field = MetadataGenericValueField(model=self._metadata_value_class)
        parser = MetadataGenericValueFieldParser(resource=value_field, query=field_data)
        try:
            evaluation_result = parser.parse(self.parse_context)
            return evaluation_result.build_clauses()
        except ReturnAll:
            return None

    def _result_for(self, check_key: str, metadata_type: MetadataTypeKey) -> Optional[EvaluationResult]:
        try:
            field = MetadataItem(metadata_type, attribute_name=check_key)
            field.resource = self.resource_field.resource
            field_parser = FieldParser(check_key, self.query[check_key], field)
            return field_parser.parse(self.parse_context)
        except ReturnAll:
            return None


class MetadataGenericValueFieldParser(NestedQueryParser):
    @property
    def _primary_key_columns(self) -> List[ColumnClause]:
        return []

    @property
    def _root_model_primary_key_columns(self) -> List[ColumnClause]:
        return []
