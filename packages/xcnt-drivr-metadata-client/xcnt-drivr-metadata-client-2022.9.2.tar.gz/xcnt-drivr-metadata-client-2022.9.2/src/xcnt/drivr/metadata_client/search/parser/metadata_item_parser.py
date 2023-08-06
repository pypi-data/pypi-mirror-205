from typing import Optional, Type

from sqlalchemy.sql import any_, select
from sqlalchemy.sql.elements import ColumnClause, or_
from sqlalchemy.sql.expression import ClauseElement
from xcnt.sqlalchemy.search import FilterFieldParser, fields
from xcnt.sqlalchemy.search.fields.scalar.base_scalar import BaseScalarField

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.model import MetadataType, MetadataValue, MetadataValueLookup
from xcnt.drivr.metadata_client.search.metadata_item import MetadataItem
from xcnt.drivr.metadata_client.search.parser.keyed_lookup_parser_mixin import KeyedLookupParserMixin

DATA_TYPE_FIELD_MAPPING = {
    DataTypeEnum.STRING: fields.Sha256String,
    DataTypeEnum.INTEGER: fields.Integer,
    DataTypeEnum.FLOAT: fields.Float,
    DataTypeEnum.BOOLEAN: fields.Boolean,
    DataTypeEnum.UUID: fields.UUID,
    DataTypeEnum.TIMESTAMP: fields.DateTime,
    # TODO: Add missing data types
}


class MetadataItemParser(FilterFieldParser[MetadataItem], KeyedLookupParserMixin):
    @classmethod
    def supports(self, entity: fields.BaseField) -> bool:
        return isinstance(entity, MetadataItem)

    @property
    def metadata_type(self) -> MetadataType:
        return self.resource_field.metadata_type

    @property
    def data_type(self) -> DataTypeEnum:
        return self.metadata_type.data_type

    @property
    def metadata_value_class(self) -> Type[MetadataValue]:
        return self.metadata_type.value_class

    @property
    def metadata_value_lookup_class(self) -> Type[MetadataValueLookup]:
        return self.metadata_type.value_lookup_class

    @property
    def entity_type(self) -> str:
        return self.metadata_type.entity_type

    @property
    def model_field(self) -> ColumnClause:
        return self.metadata_value_class.value_column_for(self.data_type)

    def _generate_metadata_type_subquery(self, clause: ClauseElement) -> ClauseElement:
        return self.model_primary_key == any_(
            select([self.metadata_value_lookup_class.entity_uuid])
            .join(
                self.metadata_value_class,
                self.metadata_value_lookup_class.metadata_value_uuid == self.metadata_value_class.uuid,
                isouter=True,
            )
            .where(self.metadata_value_lookup_class.metadata_type_uuid == self.metadata_type.uuid, clause)
            .scalar_subquery()
        )

    def filter_for(self, filter_name: str) -> Optional[ClauseElement]:
        if self.data_type not in DATA_TYPE_FIELD_MAPPING:
            return None

        clause = super().filter_for(filter_name)
        if clause is None:
            return None

        return self._generate_metadata_type_subquery(clause)

    def parse_null_filter(self) -> Optional[ClauseElement]:
        clause = super().parse_null_filter()
        if clause is None:
            return None

        value = self._extract_null_filter_value()
        if value:
            metadata_value_not_exists_clause = self.model_primary_key.not_in(
                select([self.metadata_value_lookup_class.entity_uuid]).where(
                    self.metadata_value_lookup_class.metadata_type_uuid == self.metadata_type.uuid,
                )
            )

            metadata_value_set_to_none_clause = self._generate_metadata_type_subquery(clause)

            return or_(metadata_value_not_exists_clause, metadata_value_set_to_none_clause)

        return self._generate_metadata_type_subquery(clause)

    @property
    def mapping_field(self) -> BaseScalarField:
        field_class = DATA_TYPE_FIELD_MAPPING[self.data_type]
        return field_class(self.key)
