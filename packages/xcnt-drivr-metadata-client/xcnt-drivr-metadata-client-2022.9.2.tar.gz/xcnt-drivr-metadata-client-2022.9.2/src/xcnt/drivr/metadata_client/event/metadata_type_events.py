from datetime import datetime
from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy.orm import Query, Session
from xcnt.cqrs.sqlalchemy.event import (
    Attribute,
    BatchContextManager,
    Event,
    GDPRDeleteRequestEvent,
    GDPREvent,
    TargetTable,
)

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.model import MetadataType


class BaseEvent(Event[MetadataType]):
    __abstract__ = True

    selected_entity_types: List[str] = []
    aggregate_type = "MetadataType"
    session: Session
    sqlalchemy_model: Type[MetadataType]

    @property
    def base_query(self) -> Query:
        return self.session.query(self.sqlalchemy_model).filter(self.sqlalchemy_model.uuid == self.aggregate_id)


class BaseGDPREvent(BaseEvent, GDPREvent[MetadataType]):
    __abstract__ = True

    identity_id_is_aggregate_id: bool = True


class Created(BaseEvent):
    type = "created"
    is_create = True

    entity_type: Attribute[str] = TargetTable()
    data_type: Attribute[DataTypeEnum] = TargetTable()

    def handle(self, batch_manager: Optional[BatchContextManager] = None) -> None:
        if self.entity_type in self.selected_entity_types:
            if isinstance(self.data_type, str):
                self.data_type = DataTypeEnum.from_string(self.data_type)
            super().handle(batch_manager)


class Updated(BaseEvent):
    type = "updated"

    def handle(self, _: Optional[BatchContextManager] = None) -> None:
        pass


class Deleted(BaseGDPREvent, GDPRDeleteRequestEvent[MetadataType]):
    type = "deleted"
    is_delete = True


class DomainSet(BaseEvent):
    type = "domain_set"

    domain_uuid: Attribute[UUID] = TargetTable()


class KeySet(BaseGDPREvent):
    type = "key_set"

    key: Attribute[str] = TargetTable()


class MandatorySet(BaseEvent):
    type = "mandatory_set"

    mandatory: Attribute[bool] = TargetTable()


class UniqueSet(BaseEvent):
    type = "unique_set"

    unique: Attribute[bool] = TargetTable()


class DescriptionSet(BaseGDPREvent):
    type = "description_set"

    description: Attribute[str] = TargetTable()


class BooleanDefaultValueSet(BaseEvent):
    type = "boolean_default_value_set"

    default_value: Attribute[bool] = TargetTable("default_value_boolean")


class DocumentDefaultValueSet(BaseEvent):
    type = "document_default_value_set"

    default_value: Attribute[UUID] = TargetTable("default_value_uuid")


class FloatDefaultValueSet(BaseGDPREvent):
    type = "float_default_value_set"

    default_value: Attribute[float] = TargetTable("default_value_float")


class ImageDefaultValueSet(BaseEvent):
    type = "image_default_value_set"

    default_value: Attribute[UUID] = TargetTable("default_value_uuid")


class IntegerDefaultValueSet(BaseGDPREvent):
    type = "integer_default_value_set"

    default_value: Attribute[int] = TargetTable("default_value_integer")


class StringDefaultValueSet(BaseGDPREvent):
    type = "string_default_value_set"

    default_value: Attribute[str] = TargetTable("default_value_string")


class TimestampDefaultValueSet(BaseGDPREvent):
    type = "timestamp_default_value_set"

    default_value: Attribute[datetime] = TargetTable("default_value_timestamp")


class UUIDDefaultValueSet(BaseEvent):
    type = "uuid_default_value_set"

    default_value: Attribute[UUID] = TargetTable("default_value_uuid")


ALL_METADATA_TYPE_EVENTS = (
    Created,
    Updated,
    DescriptionSet,
    Deleted,
    DomainSet,
    KeySet,
    MandatorySet,
    UniqueSet,
    BooleanDefaultValueSet,
    FloatDefaultValueSet,
    IntegerDefaultValueSet,
    StringDefaultValueSet,
    TimestampDefaultValueSet,
    UUIDDefaultValueSet,
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # DocumentDefaultValueSet,
    # ImageDefaultValueSet,
)
