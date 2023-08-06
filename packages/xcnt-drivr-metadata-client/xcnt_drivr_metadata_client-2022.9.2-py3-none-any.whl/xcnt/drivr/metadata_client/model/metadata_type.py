from typing import Any, Optional, Tuple, Type

from sqlalchemy import Boolean, Column, DateTime, Float, Index, Integer, String, func, text
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.ext.declarative import declared_attr
from webargs import fields

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.model.metadata_value import (
    INITIATED_METADATA_VALUE_CLASSES,
    INITIATED_METADATA_VALUE_LOOKUP_CLASSES,
    MetadataValue,
    MetadataValueLookup,
)

default_attribute_mapping = {
    DataTypeEnum.BOOLEAN: "default_value_boolean",
    DataTypeEnum.FLOAT: "default_value_float",
    DataTypeEnum.INTEGER: "default_value_integer",
    DataTypeEnum.STRING: "default_value_string",
    DataTypeEnum.TIMESTAMP: "default_value_timestamp",
    DataTypeEnum.UUID: "default_value_uuid",
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # DataTypeEnum.DOCUMENT: "default_value_uuid",
    # DataTypeEnum.IMAGE: "default_value_uuid",
}

webargs_fields_mapping = {
    DataTypeEnum.BOOLEAN: fields.Boolean,
    DataTypeEnum.FLOAT: fields.Float,
    DataTypeEnum.INTEGER: fields.Integer,
    DataTypeEnum.STRING: fields.String,
    DataTypeEnum.TIMESTAMP: fields.AwareDateTime,
    DataTypeEnum.UUID: fields.UUID,
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # DataTypeEnum.DOCUMENT: fields.UUID,
    # DataTypeEnum.IMAGE: fields.UUID,
}


class MetadataType:
    __tablename__ = "metadata_types"

    uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())
    domain_uuid = Column(UUID(as_uuid=True), index=True)
    entity_type = Column(String, nullable=True, index=True)
    key = Column(String, nullable=True)
    data_type = Column(ENUM(DataTypeEnum), nullable=True)
    mandatory = Column(Boolean, default=False)
    unique = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    default_value_boolean = Column(Boolean, nullable=True)
    default_value_float = Column(Float, nullable=True)
    default_value_integer = Column(Integer, nullable=True)
    default_value_string = Column(String, nullable=True)
    default_value_timestamp = Column(DateTime(timezone=True), nullable=True)
    default_value_uuid = Column(UUID(as_uuid=True), nullable=True)

    @property
    def default_value(self) -> Any:
        attribute = self._default_value_attribute
        if attribute is None:
            return None

        return getattr(self, attribute)

    @default_value.setter
    def default_value(self, value: Any) -> None:
        attribute = self._default_value_attribute
        if attribute is None:
            return None

        setattr(self, attribute, value)

    @property
    def value_class(self) -> Type[MetadataValue]:
        return INITIATED_METADATA_VALUE_CLASSES[self.entity_type]

    @property
    def value_lookup_class(self) -> Type[MetadataValueLookup]:
        return INITIATED_METADATA_VALUE_LOOKUP_CLASSES[self.entity_type]

    @property
    def _default_value_attribute(self) -> Optional[str]:
        return default_attribute_mapping.get(self.data_type, None)

    def to_webargs_field(self, is_patch: bool = False) -> fields.Field:
        field = webargs_fields_mapping.get(self.data_type, fields.String)
        required = self.mandatory
        if is_patch:
            required = False

        return field(required=required)

    @declared_attr
    def __table_args__(self) -> Tuple:
        return (Index("metadata_types_lookup_index", "domain_uuid", "entity_type"),)
