import typing
from uuid import UUID

import inflection
from marshmallow import EXCLUDE, Schema, fields
from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.lookup import (
    DRIVR_METADATA_CONTEXT_KEY,
    MetadataTypeLookup,
    register_metadata_cleanup_for,
)
from xcnt.drivr.metadata_client.marshmallow.type_field import TYPE_FIELD_LOOKUP
from xcnt.drivr.metadata_client.model import MetadataType

SCHEMA_SESSION_CACHE_KEY = "metadata_type_schemas"
SCHEMA_INSTANCE_SESSION_CACHE_KEY = "metadata_type_schema_instances"


def create_sub_fields(mapping: typing.Mapping[str, MetadataType]) -> typing.Dict[str, fields.Field]:
    sub_fields = {}
    for key, metadata_type in mapping.items():
        type_field = TYPE_FIELD_LOOKUP[metadata_type.data_type]
        sub_fields[key] = type_field(
            default=metadata_type.default_value,
            required=False,
            allow_none=not metadata_type.mandatory,
        )
    return sub_fields


def marshmallow_schema_for(entity_type: str, mapping: typing.Mapping[str, MetadataType]) -> typing.Type[Schema]:
    sub_fields = create_sub_fields(mapping)
    fields: typing.Dict[str, typing.Any] = sub_fields.copy()

    class Meta:
        unknown = EXCLUDE
        register = False

    fields["Meta"] = Meta

    return type(f"{inflection.camelize(entity_type)}MetadataField", (Schema,), fields)


def create_or_get_marshmallow_schema_for(session: Session, entity_type: str, domain_uuid: UUID) -> typing.Type[Schema]:
    register_metadata_cleanup_for(session)
    schema_cache_dict: typing.Dict[UUID, typing.Dict[str, typing.Type[Schema]]]
    schema_cache_dict = session.info.setdefault(DRIVR_METADATA_CONTEXT_KEY, {}).setdefault(SCHEMA_SESSION_CACHE_KEY, {})
    cache_dict = schema_cache_dict.setdefault(domain_uuid, {})
    if entity_type in cache_dict:
        return cache_dict[entity_type]

    lookup = MetadataTypeLookup(session=session, domain_uuid=domain_uuid, entity_type=entity_type)
    cache_dict[entity_type] = marshmallow_schema_for(entity_type, lookup.lookup_dict)
    return cache_dict[entity_type]


def create_or_get_marshmallow_schema_instance_for(session: Session, entity_type: str, domain_uuid: UUID) -> Schema:
    schema_instance_cache_dict: typing.Dict[UUID, typing.Dict[str, Schema]]
    schema_instance_cache_dict = session.info.setdefault(DRIVR_METADATA_CONTEXT_KEY, {}).setdefault(
        SCHEMA_INSTANCE_SESSION_CACHE_KEY, {}
    )
    cache_dict = schema_instance_cache_dict.setdefault(domain_uuid, {})
    if entity_type in cache_dict:
        return cache_dict[entity_type]

    # Turns out that initializing a marshmallow schema class is quite costly
    # which makes around a second in serializing 380 metadata fields. Caching
    # the instance to avoid creating the schema again
    schema_class = create_or_get_marshmallow_schema_for(session, entity_type, domain_uuid)
    schema = cache_dict[entity_type] = schema_class()
    return schema
