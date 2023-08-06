from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Type
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    cast,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.query import aliased
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import ClauseElement, select

from xcnt.drivr.metadata_client.enum import DataTypeEnum

if TYPE_CHECKING:
    from xcnt.drivr.metadata_client.model.metadata_type import MetadataType

INITIATED_METADATA_VALUE_CLASSES: Dict[str, Type[MetadataValue]] = {}
INITIATED_METADATA_VALUE_LOOKUP_CLASSES: Dict[str, Type[MetadataValueLookup]] = {}

value_mapping = {
    DataTypeEnum.BOOLEAN: "value_boolean",
    DataTypeEnum.FLOAT: "value_float",
    DataTypeEnum.INTEGER: "value_integer",
    DataTypeEnum.STRING: "value_string",
    DataTypeEnum.TIMESTAMP: "value_timestamp",
    DataTypeEnum.UUID: "value_uuid",
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # DataTypeEnum.DOCUMENT: "value_uuid",
    # DataTypeEnum.IMAGE: "value_uuid",
}


def _metadata_type_class_for(metadata_type_property: RelationshipProperty) -> Type[MetadataType]:
    return metadata_type_property.property.mapper.class_


# TODO: the resulting database table has TEN indices and insertions are prohibitively slow.
# https://drivr.atlassian.net/browse/DRIVR-1811
class MetadataValue:
    __tablename__ = "metadata_values"

    @classmethod
    def enable_metadata_type_index(cls) -> bool:
        return False

    @classmethod
    def enable_string_index_by_sha_hash(cls) -> bool:
        return False

    @classmethod
    def enable_gin_index_for_like(cls) -> bool:
        return False

    @declared_attr
    def __table_args__(self) -> Tuple[Any, ...]:
        indexes: tuple = (
            Index(
                f"{self.__tablename__}_value_boolean_index",
                self.value_boolean,
                unique=True,
                postgresql_where=self.value_boolean.isnot(None),
            ),
            Index(
                f"{self.__tablename__}_value_boolean_null_index",
                self.value_boolean,
                unique=True,
                postgresql_where=self.value_boolean.is_(None),
            ),
            Index(
                f"{self.__tablename__}_value_float_index",
                self.value_float,
                unique=True,
                postgresql_where=self.value_float.isnot(None),
            ),
            Index(
                f"{self.__tablename__}_value_float_null_index",
                self.value_float,
                unique=True,
                postgresql_where=self.value_float.is_(None),
            ),
            Index(
                f"{self.__tablename__}_value_integer_index",
                self.value_integer,
                unique=True,
                postgresql_where=self.value_integer.isnot(None),
            ),
            Index(
                f"{self.__tablename__}_value_integer_null_index",
                self.value_integer,
                unique=True,
                postgresql_where=self.value_integer.is_(None),
            ),
            Index(
                f"{self.__tablename__}_value_timestamp_index",
                self.value_timestamp,
                unique=True,
                postgresql_where=self.value_timestamp.isnot(None),
            ),
            Index(
                f"{self.__tablename__}_value_timestamp_null_index",
                self.value_timestamp,
                unique=True,
                postgresql_where=self.value_timestamp.is_(None),
            ),
            Index(
                f"{self.__tablename__}_value_uuid_index",
                self.value_uuid,
                unique=True,
                postgresql_where=self.value_uuid.isnot(None),
            ),
            Index(
                f"{self.__tablename__}_value_uuid_null_index",
                self.value_uuid,
                unique=True,
                postgresql_where=self.value_uuid.is_(None),
            ),
        )

        if self.enable_string_index_by_sha_hash():
            indexes = (  # type: ignore
                *indexes,
                Index(
                    f"{self.__tablename__}_value_string_index_hashed",
                    func.sha256(self.value_string),
                    unique=True,
                    postgresql_where=self.value_string.isnot(None),
                ),
                Index(
                    f"{self.__tablename__}_value_string_null_index_hashed",
                    func.sha256(self.value_string),
                    unique=True,
                    postgresql_where=self.value_string.is_(None),
                ),
            )
        else:
            indexes = (  # type: ignore
                *indexes,
                Index(
                    f"{self.__tablename__}_value_string_index",
                    self.value_string,
                    unique=True,
                    postgresql_where=self.value_string.isnot(None),
                ),
                Index(
                    f"{self.__tablename__}_value_string_null_index",
                    self.value_string,
                    unique=True,
                    postgresql_where=self.value_string.is_(None),
                ),
            )

        if self.enable_gin_index_for_like():
            indexes = (
                *indexes,
                Index(
                    f"{self.__tablename__}_value_string_gin_index",
                    cast(self.value_string, String).label("value_string"),
                    postgresql_using="gin",
                    postgresql_ops={
                        "value_string": "gin_trgm_ops",
                    },
                ),
                Index(
                    f"{self.__tablename__}_value_string_uuid_gin_index",
                    func.regexp_replace(cast(self.value_uuid, String), "[^a-f0-9]", "", "g").label("value_uuid"),
                    postgresql_using="gin",
                    postgresql_ops={
                        "value_uuid": "gin_trgm_ops",
                    },
                ),
            )

        return indexes

    uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid4)
    value_boolean = Column(Boolean, nullable=True)
    value_float = Column(Float, nullable=True)
    value_integer = Column(Integer, nullable=True)
    value_string = Column(String, nullable=True)
    value_timestamp = Column(DateTime(timezone=True), nullable=True)
    value_uuid = Column(UUID(as_uuid=True), nullable=True)

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())

    @classmethod
    def value_column_name_for(cls, current_type: DataTypeEnum) -> str:
        return value_mapping[current_type]

    @classmethod
    def value_column_for(cls, current_type: DataTypeEnum) -> Column:
        column_name = cls.value_column_name_for(current_type)
        return getattr(cls, column_name)

    def get_value(self, data_type: DataTypeEnum) -> Optional[Any]:
        return getattr(self, self.value_column_name_for(data_type))

    def set_value(self, value: Optional[Any], data_type: DataTypeEnum) -> None:
        converted_value = self._convert_value(value, data_type)
        setattr(self, self.value_column_name_for(data_type), converted_value)

    def _convert_value(self, value: Optional[Any], data_type: DataTypeEnum) -> Optional[Any]:
        if data_type == DataTypeEnum.TIMESTAMP and isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
        return value


class MetadataValueLookup:
    __tablename__ = "metadata_values_lookup"

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())

    @classmethod
    def enable_value_index(cls) -> bool:
        return True

    @declared_attr
    def __table_args__(self) -> Tuple[Any, ...]:
        indexes: tuple = (
            UniqueConstraint("entity_uuid", "metadata_type_uuid", name=f"{self.__tablename__}_unique_constraint"),
            PrimaryKeyConstraint("entity_uuid", "metadata_type_uuid", name=f"{self.__tablename__}_primary_key"),
        )

        if self.enable_value_index():
            indexes = (  # type: ignore
                *indexes,
                Index(
                    f"{self.__tablename__}_metadata_value_uuid_index",
                    self.metadata_value_uuid,
                    self.metadata_type_uuid,
                    self.entity_uuid,
                ),
            )

        return indexes

    @property
    def entity_uuid(self) -> Column:
        pass

    @property
    def entity(self) -> RelationshipProperty:
        pass

    @property
    def metadata_value_uuid(self) -> Column:
        pass

    @property
    def metadata_value(self) -> RelationshipProperty:
        pass

    @property
    def value(self) -> Any | None:
        value_attribute_name = self.metadata_value.value_column_name_for(self._current_type)
        return self._value(value_attribute_name)

    @property
    def value_string(self) -> Any | None:
        return self._value("value_string")

    @property
    def value_integer(self) -> Any | None:
        return self._value("value_integer")

    @property
    def value_float(self) -> Any | None:
        return self._value("value_float")

    @property
    def value_boolean(self) -> Any | None:
        return self._value("value_boolean")

    @property
    def value_timestamp(self) -> Any | None:
        return self._value("value_timestamp")

    @property
    def value_uuid(self) -> Any | None:
        return self._value("value_uuid")

    def _value(self, value_attribute_name: str) -> Any | None:
        return getattr(self.metadata_value, value_attribute_name)

    @declared_attr
    def metadata_type_uuid(self) -> Column:
        return Column(
            UUID(as_uuid=True),
            ForeignKey(
                "metadata_types.uuid",
                name=f"fk_{self.__tablename__}_metadata_type_uuid",
                onupdate="CASCADE",
                ondelete="CASCADE",
            ),
            index=False,
        )

    @declared_attr
    def metadata_type(self) -> RelationshipProperty:
        return relationship("MetadataType", lazy="joined")

    @hybrid_property
    def _current_type(self) -> DataTypeEnum:
        return self.metadata_type.data_type

    @_current_type.expression  # type: ignore
    def _current_type(self) -> ClauseElement:
        metadata_type_class = aliased(_metadata_type_class_for(self.metadata_type))
        return (
            select([metadata_type_class.data_type])
            .where(self.metadata_type_uuid == metadata_type_class.uuid)
            .label("key")
        )

    @hybrid_property
    def key(self) -> str:
        return getattr(self.metadata_type, "key", None)

    @key.expression  # type: ignore
    def key(self) -> ClauseElement:
        metadata_type_class = aliased(_metadata_type_class_for(self.metadata_type))
        return select([metadata_type_class.key]).where(self.metadata_type_uuid == metadata_type_class.uuid).label("key")
