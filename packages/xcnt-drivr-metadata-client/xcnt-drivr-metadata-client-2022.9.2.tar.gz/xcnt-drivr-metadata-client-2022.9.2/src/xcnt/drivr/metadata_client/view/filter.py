import inspect
from functools import cached_property
from typing import Any, Callable, Dict, List, Mapping, Optional, Type, Union, cast
from uuid import UUID

import mujson
from marshmallow import INCLUDE, Schema, ValidationError
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import ClauseElement, ColumnElement
from webargs import fields
from webargs.core import Parser

from xcnt.drivr.metadata_client.configuration import INITIATED_METADATA_VALUE_LOOKUP_CLASSES
from xcnt.drivr.metadata_client.view.sqlalchemy_list_web_args_builder import SqalchemyListWebArgsBuilder

parser = Parser(unknown=INCLUDE)


class MetadataFilter:
    def __init__(self, entity_type: str, domain_uuid: UUID, metadata_field_name: str = "metadata"):
        self.entity_type = entity_type
        self.domain_uuid = domain_uuid
        self.metadata_field_name = metadata_field_name

    @cached_property
    def web_args_builder(self) -> SqalchemyListWebArgsBuilder:
        return SqalchemyListWebArgsBuilder(self.entity_type)

    def _generate_webargs(self) -> Mapping[str, Union[type, fields.Field]]:
        return self.web_args_builder.fields_for(self.domain_uuid)

    def _extract_metadata(self, item: Dict[str, Any]) -> Dict[str, Any]:
        metadata_field_name = self.metadata_field_name
        metadata_query: Dict[str, Any]
        if metadata_field_name not in item:
            return {}
        metadata_candidate: Optional[Union[str, Dict[str, Any]]] = item[metadata_field_name]

        if metadata_candidate is None:
            return {}

        elif isinstance(metadata_candidate, str):
            try:
                metadata_query = mujson.loads(metadata_candidate)
            except ValueError:
                message = (
                    f"Unsupported field for metadata in key {metadata_field_name}. String could not be decoded to JSON."
                )
                raise ValidationError({metadata_field_name: message})
        elif isinstance(metadata_candidate, dict):
            metadata_query = metadata_candidate
        else:
            message = (
                "Unsupported type for metadata decoding. Needs to be a JSON parseable string or a nested argument."
            )
            raise ValidationError({metadata_field_name: message})

        if not isinstance(metadata_query, dict):
            raise ValidationError({metadata_field_name: "Metadata must be decodable to a dict."})

        return metadata_query

    def _filter_by_webargs(self, item: Dict[str, Any]) -> ClauseElement:
        metadata_query_config = self._extract_metadata(item)
        schema = Schema.from_dict(dict(self._generate_webargs()))
        try:
            parsed_fields: Dict[str, ColumnElement] = schema().load(metadata_query_config)
        except ValidationError as validation_error:
            raise ValidationError({self.metadata_field_name: validation_error.messages})
        clause_elements: List[ColumnElement] = list(parsed_fields.values())
        filters: List[ClauseElement] = []
        for clause_element in clause_elements:
            filters.append(self.metadata_entity_uuid_column.in_(clause_element))

        if len(filters) == 0:
            return and_(True)

        return and_(*filters)

    @property
    def metadata_entity_uuid_column(self) -> Type[ColumnElement]:
        return getattr(self.metadata_entity_class, "uuid")

    @property
    def metadata_entity_class(self) -> Type[declarative_base]:
        relation = INITIATED_METADATA_VALUE_LOOKUP_CLASSES[self.entity_type].entity
        relation_property = getattr(relation, "property")
        return cast(Type[declarative_base], relation_property.mapper.class_)

    def filter(self) -> Callable[[Dict[str, Any]], ClauseElement]:
        return self._filter_by_webargs


def filter_for(
    entity_type: Union[str, Type], domain_uuid: UUID, metadata_field_name: str = "metadata"
) -> Callable[[Dict[str, Any]], ClauseElement]:
    if inspect.isclass(entity_type):
        entity_type = cast(Type, entity_type).__name__
    assert isinstance(entity_type, str)

    metadata_filter = MetadataFilter(
        entity_type=entity_type, domain_uuid=domain_uuid, metadata_field_name=metadata_field_name
    )
    return metadata_filter.filter()
