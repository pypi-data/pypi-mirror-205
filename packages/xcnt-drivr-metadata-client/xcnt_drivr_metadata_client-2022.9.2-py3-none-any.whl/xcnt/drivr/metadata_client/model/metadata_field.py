from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Any, Dict, MutableMapping, Optional, Type, Union
from uuid import UUID, uuid4
from weakref import ReferenceType, WeakKeyDictionary, ref

from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.lookup import (
    DRIVR_METADATA_CONTEXT_KEY,
    MetadataTypeLookup,
    register_metadata_cleanup_for,
)
from xcnt.drivr.metadata_client.model.metadata_value import (
    INITIATED_METADATA_VALUE_CLASSES,
    INITIATED_METADATA_VALUE_LOOKUP_CLASSES,
    MetadataValue,
    MetadataValueLookup,
)

if TYPE_CHECKING:
    from xcnt.drivr.metadata_client.model.metadata_type import MetadataType

DRIVR_METADATA_FIELD_CACHE_KEY = "drivr-metadata-model-field-cache"
DRIVR_METADATA_TYPES_CACHE_KEY = "drivr-metadata-types-cache"


class InstantiatedMetadataFieldMeta(type):
    _session: Session

    @property
    def session(self) -> Session:
        return self._session

    @session.setter
    def session(self, value: Session) -> None:
        register_metadata_cleanup_for(value)
        self._session = value


def get_cached_lookup(session: Session, domain_uuid: UUID, entity_type: str) -> MetadataTypeLookup:
    """Returns existing or new :class:`MetadataTypeLookup` from per-session scoped cache."""
    key = (domain_uuid, entity_type)
    cache = session.info.setdefault(DRIVR_METADATA_TYPES_CACHE_KEY, {})
    if key not in cache:
        cache[key] = MetadataTypeLookup(session, domain_uuid, entity_type)
    return cache[key]


class InstantiatedMetadataField(metaclass=InstantiatedMetadataFieldMeta):
    def __init__(self, instance: Any, entity_type: str, domain_uuid: UUID, entity_uuid: UUID):
        self._instance = instance
        self._entity_type = entity_type
        self._domain_uuid = domain_uuid
        self._entity_uuid = entity_uuid
        self._lookup = get_cached_lookup(self.__class__.session, self._domain_uuid, self._entity_type)

    def __getattr__(self, name: str) -> Any:
        self._verify_for_attribute(name)
        return self._retrieve(self._metadata_type_dict[name])

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
            return

        self._verify_for_attribute(name)
        self._store(self._metadata_type_dict[name], value)

    def _verify_for_attribute(self, name: str) -> None:
        if name not in self._metadata_type_dict:
            raise AttributeError(f"No attribute {name} registered")

    @property
    def _metadata_type_dict(self) -> Dict[str, MetadataType]:
        return self._lookup.lookup_dict

    def _store(self, metadata_type: MetadataType, value: Any | None) -> None:
        self._request_values_if_necessary()
        session = self.__class__.session

        null_value_columns = {column.key: None for column in self.value_table.c if column.name.startswith("value")}
        column_clauses = {key: self.value_table.c[key].is_(None) for key in null_value_columns}
        value_column = self._value_class.value_column_name_for(metadata_type.data_type)
        column_clauses[value_column] = self.value_table.c[value_column] == value

        try:
            metadata_value = session.query(self._value_class).where(*column_clauses.values()).one()
        except Exception:
            metadata_value = self._value_class(uuid=uuid4())  # type: ignore
            metadata_value.set_value(value, metadata_type.data_type)
            session.execute(
                insert(self.value_table)
                .values(
                    uuid=metadata_value.uuid,
                    value_string=metadata_value.value_string,
                    value_integer=metadata_value.value_integer,
                    value_float=metadata_value.value_float,
                    value_boolean=metadata_value.value_boolean,
                    value_timestamp=metadata_value.value_timestamp,
                    value_uuid=metadata_value.value_uuid,
                )
                .on_conflict_do_nothing()
            )

        lookup_dict = self._value_lookup_dict
        if metadata_type not in lookup_dict:
            metadata_lookup = self._value_lookup_class(  # type: ignore
                entity_uuid=self._entity_uuid,
                metadata_value=metadata_value,
                metadata_type=metadata_type,
            )
            lookup_dict[metadata_type] = metadata_lookup
            self._value_lookup_dict = lookup_dict
            session.execute(
                insert(self.lookup_table)
                .values(
                    entity_uuid=self._entity_uuid,
                    metadata_value_uuid=metadata_value.uuid,
                    metadata_type_uuid=metadata_type.uuid,
                )
                .on_conflict_do_update(
                    index_elements=[self.lookup_table.c.entity_uuid, self.lookup_table.c.metadata_type_uuid],
                    set_={
                        "metadata_value_uuid": metadata_value.uuid,
                    },
                )
            )

        metadata_lookup = self._value_lookup_dict[metadata_type]
        metadata_lookup.metadata_value = metadata_value  # type: ignore

    def _retrieve(self, metadata_type: MetadataType) -> Optional[Any]:
        self._request_values_if_necessary()
        metadata_value = self._value_lookup_dict.get(metadata_type, None)
        return getattr(metadata_value, "value", None)

    @property
    def _value_class(self) -> Type[MetadataValue]:
        return INITIATED_METADATA_VALUE_CLASSES[self._entity_type]

    @property
    def value_table(self) -> Table:
        return self._value_class.__table__  # type: ignore

    @property
    def _value_lookup_class(self) -> Type[MetadataValueLookup]:
        return INITIATED_METADATA_VALUE_LOOKUP_CLASSES[self._entity_type]

    @property
    def lookup_table(self) -> Table:
        return self._value_lookup_class.__table__  # type: ignore

    @property
    def _key_cache(self) -> Dict[Any, Dict[MetadataType, MetadataValueLookup]]:
        session = self.__class__.session
        global_cache = session.info.setdefault(DRIVR_METADATA_CONTEXT_KEY, {})
        if DRIVR_METADATA_FIELD_CACHE_KEY not in global_cache:
            global_cache[DRIVR_METADATA_FIELD_CACHE_KEY] = WeakKeyDictionary()
        return global_cache[DRIVR_METADATA_FIELD_CACHE_KEY]

    @property
    def _values_requested(self) -> bool:
        return self._instance in self._key_cache

    @property
    def _value_lookup_dict(self) -> Dict[MetadataType, MetadataValueLookup]:
        return self._key_cache.get(self._instance, {})

    @_value_lookup_dict.setter
    def _value_lookup_dict(self, values: Dict[MetadataType, MetadataValueLookup]) -> None:
        self._key_cache[self._instance] = values

    def _to_dict(self) -> Dict[str, Any]:
        return dict((key, self._retrieve(metadata_type)) for key, metadata_type in self._metadata_type_dict.items())

    def _request_values_if_necessary(self) -> None:
        if self._values_requested:
            return
        values = self._instance.metadata_values
        self._value_lookup_dict = dict((value.metadata_type, value) for value in values)


class MetadataField:
    _metadata_field_cache: MutableMapping[Any, ReferenceType[InstantiatedMetadataField]]

    def __init__(self, entity_type: str, domain_uuid: str, uuid_field: str = "uuid"):
        self._entity_type = entity_type
        self._domain_uuid = domain_uuid
        self._uuid_field = uuid_field
        self._metadata_field_cache = WeakKeyDictionary()

    def __get__(self, instance: Optional[Any], owner: Optional[Any]) -> Union[InstantiatedMetadataField, MetadataField]:
        if instance is None:
            return self

        # This issues a WeakKeyValueDictionary, ensuring that no references are kept if the caching dict
        # is the only reference to the model or the metadata field.
        metadata_field: Optional[InstantiatedMetadataField] = None
        if instance in self._metadata_field_cache:
            metadata_field_ref = self._metadata_field_cache[instance]
            metadata_field = metadata_field_ref()

        if metadata_field is None:
            metadata_field = InstantiatedMetadataField(
                entity_type=self._entity_type,
                domain_uuid=getattr(instance, self._domain_uuid),
                entity_uuid=getattr(instance, self._uuid_field),
                instance=instance,
            )

            def remove_logic(weakref: ReferenceType[InstantiatedMetadataField], instance: Any) -> None:
                self._remove_for(instance)

            metadata_field_ref = ref(metadata_field, partial(remove_logic, instance=instance))
            self._metadata_field_cache[instance] = metadata_field_ref
        return metadata_field

    def _remove_for(self, instance: Any) -> None:
        try:
            del self._metadata_field_cache[instance]
        except KeyError:
            pass
