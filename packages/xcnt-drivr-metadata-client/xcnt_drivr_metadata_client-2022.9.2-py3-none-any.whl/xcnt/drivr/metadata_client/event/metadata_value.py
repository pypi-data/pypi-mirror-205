from abc import abstractproperty
from collections import defaultdict
from datetime import datetime, timezone
from queue import Queue
from typing import Any, Iterable, List, MutableMapping, Optional, Type, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import Table, select
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Mapper, Query
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import Column
from xcnt.cqrs.sqlalchemy.event import Attribute, BatchContextManager, Event, GDPREvent, bulk_db_for
from xcnt.cqrs.sqlalchemy.event.db_handler.base import EnsureForeignKeyModel
from xcnt.cqrs.sqlalchemy.event.db_handler.bulk import BulkDB

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.model import MetadataType

CONCRETE_METADATA_VALUE_EVENTS: MutableMapping[str, MutableMapping[str, Type[Event]]]
CONCRETE_METADATA_VALUE_EVENTS = defaultdict(lambda: {})
SQLAlchemyModel = TypeVar("SQLAlchemyModel")


def _enforce_timezone(item: Optional[datetime]) -> Optional[datetime]:
    if item is not None and item.tzinfo is None:
        item = item.astimezone(timezone.utc)
    return item


def _ensure_utc(item: Optional[datetime]) -> Optional[datetime]:
    if isinstance(item, datetime) and item.tzinfo is not None:
        item = item.astimezone(timezone.utc).replace(tzinfo=None)
    return item


class BaseEvent(Event[SQLAlchemyModel]):
    __abstract__ = True
    is_bulk_compatible = True

    metadata_type_uuid: Attribute[UUID]
    sqlalchemy_model: DeclarativeMeta
    value: Attribute[Any]
    session: Session

    @abstractproperty
    def _value_column(self) -> str:
        pass

    @property
    def value_model(self) -> Mapper:
        return self.sqlalchemy_model.metadata_value.mapper

    @property
    def value_table(self) -> Table:
        return self.value_model.tables[0]

    @property
    def metadata_type_table(self) -> Table:
        return self.sqlalchemy_model.metadata.tables[MetadataType.__tablename__]

    @property
    def metadata_type_foreign_key_insert(self) -> EnsureForeignKeyModel:
        return EnsureForeignKeyModel(
            self.metadata_type_table,
            self.metadata_type_table.c.uuid,
            self.metadata_type_uuid,
        )

    @property
    def metadata_value_foreign_key_insert(self) -> EnsureForeignKeyModel:
        return EnsureForeignKeyModel(
            self.value_table,
            self.value_table.c.uuid,
            uuid4(),
            {self._value_column: self.escaped_value},
        )

    @property
    def _foreign_key_models(self) -> Iterable[EnsureForeignKeyModel]:
        target_property = self.sqlalchemy_model.entity.property  # type: ignore
        remote_columns = list(target_property.remote_side)
        check: "Queue[Column]" = Queue()

        insert_columns: List[Column] = []
        if len(remote_columns) == 1:
            remote_column = set(remote_columns).pop()
            check.put(remote_column)
            insert_columns.append(remote_column)

        while not check.empty():
            check_item = check.get()
            for foreign_key in check_item.foreign_keys:
                insert_columns.append(foreign_key.column)
                check.put(foreign_key.column)

        for insert_column in insert_columns[::-1]:
            yield EnsureForeignKeyModel(
                insert_column.table,
                pk_column=insert_column,
                pk_value=self.aggregate_id,
            )

    @property
    def value_query(self) -> Query:
        null_value_columns = {column.key: None for column in self.value_table.c if column.name.startswith("value")}
        column_clauses = {key: self.value_table.c[key].is_(None) for key in null_value_columns}
        column_clauses[self._value_column] = self.value_table.c[self._value_column] == self.escaped_value
        return select(self.value_table.c.uuid.label("metadata_value_uuid")).where(*column_clauses.values()).limit(1)

    def _ensure_remotes(self, bulk_db_handler: BulkDB) -> None:
        for foreign_key_model in self._foreign_key_models:
            bulk_db_handler.add_foreign_key_insert_for(foreign_key_model)
        bulk_db_handler.add_foreign_key_insert_for(self.metadata_type_foreign_key_insert)
        bulk_db_handler.add_foreign_key_insert_for(self.metadata_value_foreign_key_insert)

    def handle(self, batch_manager: Optional[BatchContextManager] = None) -> None:
        assert batch_manager is not None
        bulk_db_handler = bulk_db_for(batch_manager=batch_manager, session=self.__class__.session)
        self._ensure_remotes(bulk_db_handler)

        bulk_db_handler.add_insert_for(
            self.sqlalchemy_model,
            {
                "entity_uuid": self.aggregate_id,
                "metadata_type_uuid": self.metadata_type_uuid,
                "metadata_value_uuid": self.value_query,
            },
        )

    @property
    def escaped_value(self) -> Any:
        return self.value


class BaseGDPREvent(GDPREvent[SQLAlchemyModel], BaseEvent):
    __abstract__ = True

    identity_id_is_aggregate_id: bool = True


class MetadataBooleanSet(BaseEvent):
    __abstract__ = True

    type = "metadata_value_boolean_set"

    value: Attribute[bool]

    @property
    def _value_column(self) -> str:
        return "value_boolean"


class MetadataDocumentSet(BaseEvent):
    __abstract__ = True

    type = "metadata_value_document_set"

    value: Attribute[UUID]

    @property
    def _value_column(self) -> str:
        return "value_uuid"


class MetadataFloatSet(BaseGDPREvent[SQLAlchemyModel]):
    __abstract__ = True

    type = "metadata_value_float_set"

    value: Attribute[float]

    @property
    def _value_column(self) -> str:
        return "value_float"


class MetadataIntegerSet(BaseGDPREvent[SQLAlchemyModel]):
    __abstract__ = True

    type = "metadata_value_integer_set"

    value: Attribute[int]

    @property
    def _value_column(self) -> str:
        return "value_integer"


class MetadataImageSet(BaseEvent):
    __abstract__ = True

    type = "metadata_value_image_set"

    value: Attribute[UUID]

    @property
    def _value_column(self) -> str:
        return "value_uuid"


class MetadataStringSet(BaseGDPREvent[SQLAlchemyModel]):
    __abstract__ = True

    type = "metadata_value_string_set"

    value: Attribute[str]

    @property
    def _value_column(self) -> str:
        return "value_string"


class MetadataTimestampSet(BaseGDPREvent[SQLAlchemyModel]):
    __abstract__ = True

    type = "metadata_value_timestamp_set"

    value: Attribute[datetime]

    @property
    def _value_column(self) -> str:
        return "value_timestamp"

    @property
    def escaped_value(self) -> Any:
        return _enforce_timezone(self.value)


class MetadataUUIDSet(BaseEvent):
    __abstract__ = True

    type = "metadata_value_uuid_set"

    value: Attribute[UUID]

    @property
    def _value_column(self) -> str:
        return "value_uuid"


ALL_METADATA_VALUE_EVENTS = (
    MetadataBooleanSet,
    MetadataFloatSet,
    MetadataIntegerSet,
    MetadataStringSet,
    MetadataTimestampSet,
    MetadataUUIDSet,
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # MetadataDocumentSet,
    # MetadataImageSet,
)


METADATA_VALUE_TYPE_BY_DATA_TYPE_ENUM = {
    DataTypeEnum.BOOLEAN: MetadataBooleanSet.type,
    DataTypeEnum.FLOAT: MetadataFloatSet.type,
    DataTypeEnum.INTEGER: MetadataIntegerSet.type,
    DataTypeEnum.STRING: MetadataStringSet.type,
    DataTypeEnum.TIMESTAMP: MetadataTimestampSet.type,
    DataTypeEnum.UUID: MetadataUUIDSet.type,
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # DataTypeEnum.DOCUMENT: MetadataDocumentSet.type,
    # DataTypeEnum.IMAGE: MetadataImageSet.type,
}
