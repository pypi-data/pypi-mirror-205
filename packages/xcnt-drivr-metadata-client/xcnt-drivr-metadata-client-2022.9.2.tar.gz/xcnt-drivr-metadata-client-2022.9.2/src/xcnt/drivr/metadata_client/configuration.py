from typing import Any, Iterable, Mapping, Optional, Type, cast

import inflection
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session, backref, relationship
from xcnt.cqrs.event import Event, Registry

from xcnt.drivr.metadata_client.enum import MetadataValueFeatureEnum
from xcnt.drivr.metadata_client.event import ALL_METADATA_VALUE_EVENTS, CONCRETE_METADATA_VALUE_EVENTS
from xcnt.drivr.metadata_client.event.metadata_type_events import BaseEvent
from xcnt.drivr.metadata_client.lookup import MetadataTypeLookup
from xcnt.drivr.metadata_client.model import (
    INITIATED_METADATA_VALUE_CLASSES,
    INITIATED_METADATA_VALUE_LOOKUP_CLASSES,
    MetadataType,
    MetadataValue,
    MetadataValueLookup,
)
from xcnt.drivr.metadata_client.model.metadata_field import InstantiatedMetadataField


def metadata_type_model_for(declarative_base: DeclarativeMeta, session: Session) -> Type[MetadataType]:
    initialized_metadata_type = type("MetadataType", (MetadataType, declarative_base), {})
    BaseEvent.sqlalchemy_model = cast(Type[MetadataType], initialized_metadata_type)
    BaseEvent.session = session
    MetadataTypeLookup.metadata_type = initialized_metadata_type
    InstantiatedMetadataField.session = session

    return initialized_metadata_type


def metadata_value_model_for(
    declarative_base: DeclarativeMeta,
    entity_type: str,
    reference_model: Any,
    features: Optional[Iterable[MetadataValueFeatureEnum]] = None,
) -> tuple[Type[MetadataValue], Type[MetadataValueLookup]]:
    if features is not None:
        features = list(features)

    value_class_name = f"{inflection.camelize(entity_type)}MetadataValue"
    value_lookup_class_name = f"{inflection.camelize(entity_type)}MetadataValueLookup"
    reference_table_name = getattr(reference_model, "__tablename__")
    value_table_name = inflection.underscore(value_class_name)
    value_lookup_table_name = inflection.underscore(value_lookup_class_name)

    metadata_value_attributes = {
        "__tablename__": value_table_name,
    }
    metadata_value_lookup_attributes = {
        "__tablename__": value_lookup_table_name,
        "metadata_value_uuid": Column(
            PostgreSQLUUID(as_uuid=True),
            ForeignKey(
                f"{value_table_name}.uuid",
                name=f"fk_{value_table_name}_lookup_uuid",
                onupdate="CASCADE",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        ),
        "metadata_value": relationship(value_class_name, lazy="joined"),
        "entity_uuid": Column(
            PostgreSQLUUID(as_uuid=True),
            ForeignKey(
                f"{reference_table_name}.uuid",
                name=f"fk_{value_lookup_table_name}_{reference_table_name}_uuid",
                onupdate="CASCADE",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        ),
        "entity": relationship(
            reference_model,
            uselist=False,
            lazy="joined",
            backref=backref("metadata_values", uselist=True, lazy="selectin"),
        ),
    }

    if features is not None and len(features) > 0:
        if MetadataValueFeatureEnum.DISABLE_VALUE_INDEXES in features:
            metadata_value_lookup_attributes["enable_value_index"] = lambda: False
        if MetadataValueFeatureEnum.ENABLE_METADATA_TYPE_INDEX in features:
            metadata_value_attributes["enable_metadata_type_index"] = lambda: True
        if MetadataValueFeatureEnum.ENABLE_STRING_INDEX_BY_SHA_HASH in features:
            metadata_value_attributes["enable_string_index_by_sha_hash"] = lambda: True
        if MetadataValueFeatureEnum.ENABLE_GIN_INDEX_FOR_LIKE in features:
            metadata_value_attributes["enable_gin_index_for_like"] = lambda: True

    initialized_metadata_value = type(
        value_class_name,
        (MetadataValue, declarative_base),
        metadata_value_attributes,
    )
    initialized_metadata_value_lookup = type(
        value_lookup_class_name,
        (MetadataValueLookup, declarative_base),
        metadata_value_lookup_attributes,
    )
    INITIATED_METADATA_VALUE_CLASSES[entity_type] = initialized_metadata_value
    INITIATED_METADATA_VALUE_LOOKUP_CLASSES[entity_type] = initialized_metadata_value_lookup
    BaseEvent.selected_entity_types.append(entity_type)
    return initialized_metadata_value, initialized_metadata_value_lookup


def register_metadata_events_for(
    registry: Registry, reference_model: Any, entity_type: str, session: Session
) -> Mapping[str, Type[Event]]:
    event_mapping = CONCRETE_METADATA_VALUE_EVENTS[entity_type]
    for metadata_value_event in ALL_METADATA_VALUE_EVENTS:
        event_name = f"{inflection.camelize(entity_type)}{metadata_value_event.__name__}"
        concrete_metadata_value_event = type(
            event_name,
            (metadata_value_event,),
            {
                "aggregate_type": inflection.camelize(entity_type),
                "sqlalchemy_model": reference_model,
                "session": session,
            },
        )
        registry.register(concrete_metadata_value_event)
        event_mapping[concrete_metadata_value_event.type] = concrete_metadata_value_event  # type: ignore
    return event_mapping
