import typing
from uuid import UUID

import inflection
from marshmallow import EXCLUDE, RAISE, Schema, fields
from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.lookup import MetadataTypeLookup, register_metadata_cleanup_for
from xcnt.drivr.metadata_client.marshmallow.type_field import DATA_TYPE_INPUT_FIELD_MAPPING, TYPE_FIELD_LOOKUP
from xcnt.drivr.metadata_client.model import MetadataType


class MetadataKeyValuePairSchema(Schema):
    key = fields.Str()
    metadata_type_uuid = fields.UUID(dump_only=True)
    data_type = fields.Str(dump_only=True)


def _get_metadata_value_schema_for(entity_type: str, metadata_type: MetadataType) -> Schema:
    class Meta:
        unknown = RAISE
        register = False

    cls_fields = {}
    cls_fields["Meta"] = Meta
    type_field = TYPE_FIELD_LOOKUP[metadata_type.data_type]
    cls_fields[DATA_TYPE_INPUT_FIELD_MAPPING[metadata_type.data_type]] = type_field(
        default=metadata_type.default_value,
        required=True,
        allow_none=not metadata_type.mandatory,
    )
    return type(
        f"{inflection.camelize(entity_type)}MetadataValue{inflection.camelize(str(metadata_type.data_type))}",
        (Schema,),
        cls_fields,
    )


def _create_key_value_pairs_for(
    entity_type: str, mapping: typing.Mapping[str, MetadataType], loader_schema: bool
) -> dict[str, fields.Field]:
    key_value_pairs = {}

    for key, metadata_type in mapping.items():

        class Meta:
            unknown = EXCLUDE
            register = False

        cls_fields = {}
        cls_fields["Meta"] = Meta

        if loader_schema:
            valuefield = _get_metadata_value_schema_for(entity_type, metadata_type)
            cls_fields["value"] = fields.Nested(valuefield, required=True)
        else:
            cls_fields["value"] = TYPE_FIELD_LOOKUP[metadata_type.data_type](
                default=metadata_type.default_value,
                required=False,
                allow_none=not metadata_type.mandatory,
            )

        key_value_pairs[key] = type(
            f"{inflection.camelize(entity_type)}MetadataKeyValuePair"
            "{inflection.camelize(str(metadata_type.data_type))}",
            (MetadataKeyValuePairSchema,),
            cls_fields,
        )

    return key_value_pairs


def create_key_value_pairs_for(
    session: Session,
    entity_type: str,
    domain_uuid: UUID,
    loader_schema: bool = False,
) -> dict[str, fields.Field]:
    register_metadata_cleanup_for(session)
    lookup = MetadataTypeLookup(session=session, domain_uuid=domain_uuid, entity_type=entity_type)
    return _create_key_value_pairs_for(entity_type, lookup.lookup_dict, loader_schema)
