from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, Type

from sqlalchemy.orm import Session
from xcnt.cqrs.event import Event

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.event import CONCRETE_METADATA_VALUE_EVENTS, METADATA_VALUE_TYPE_BY_DATA_TYPE_ENUM
from xcnt.drivr.metadata_client.lookup import MetadataLookup
from xcnt.drivr.metadata_client.model import MetadataType
from xcnt.drivr.metadata_client.model.metadata_field import InstantiatedMetadataField

if TYPE_CHECKING:
    from xcnt.drivr.metadata_client.command.metadata_value_command import MetadataValueCommand


class MetadataExecution:
    def __init__(self, command: MetadataValueCommand):
        self._command = command
        self._lookup = MetadataLookup(
            session=self.session,
            entity_type=self._command.metadata_entity_type,
            domain_uuid=self._command.metadata_domain_uuid,
            entity_uuid=self._command.aggregate_id,
        )

    @property
    def session(self) -> Session:
        return self._command.session

    @property
    def metadata(self) -> Dict[str, Any]:
        metadata = getattr(self._command, "metadata", None)
        if not metadata:
            return {}
        if isinstance(metadata, InstantiatedMetadataField):
            return metadata._to_dict()
        return metadata

    @cached_property
    def metadata_events(self) -> Dict[DataTypeEnum, Type[Event]]:
        type_lookup = CONCRETE_METADATA_VALUE_EVENTS[self._command.metadata_entity_type]
        return dict(
            (data_type, type_lookup[metadata_event_type])
            for data_type, metadata_event_type in METADATA_VALUE_TYPE_BY_DATA_TYPE_ENUM.items()
        )

    @property
    def metadata_types(self) -> Dict[str, MetadataType]:
        return self._lookup.types

    @property
    def metadata_value_dict(self) -> Dict[str, Any]:
        return self._lookup.values

    def generate_events(self) -> Iterable[Event]:
        for key, metadata_type in self.metadata_types.items():
            event = self._event_for(key, metadata_type)
            if event is not None:
                yield event

    def _event_for(self, key: str, metadata_type: MetadataType) -> Optional[Event]:
        if key not in self.metadata:
            if key in self.metadata_value_dict:
                value = self.metadata_value_dict[key]
            elif metadata_type.default_value is not None:
                value = metadata_type.default_value
            else:
                return None
        else:
            value = self.metadata[key]

        if key in self.metadata_value_dict and self.metadata_value_dict[key] == value:
            return None

        event_class = self.metadata_events[metadata_type.data_type]
        event = event_class(aggregate_id=self._command.aggregate_id, metadata_type_uuid=metadata_type.uuid, value=value)
        return event
