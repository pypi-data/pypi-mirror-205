from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Type, cast
from uuid import UUID
from weakref import WeakSet

from sqlalchemy import and_, event
from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.model.metadata_type import MetadataType

DRIVR_METADATA_CONTEXT_KEY = "drivr_metadata"
DRIVR_METADATA_ENTITY_TYPE_KEY = "entity_types"


SESSIONS_WHICH_ARE_REGISTERED: Set[Session] = cast(Set[Session], WeakSet())


def register_metadata_cleanup_for(session: Session) -> None:
    if session in SESSIONS_WHICH_ARE_REGISTERED:
        return

    @event.listens_for(session, "after_rollback")
    @event.listens_for(session, "after_commit")
    @event.listens_for(session, "after_soft_rollback")
    @event.listens_for(session, "after_begin")
    @event.listens_for(session, "after_flush")
    def cleanup_session_info(session: Session, *args: Any) -> None:
        if DRIVR_METADATA_CONTEXT_KEY in session.info:
            del session.info[DRIVR_METADATA_CONTEXT_KEY]

    SESSIONS_WHICH_ARE_REGISTERED.add(session)


class MetadataTypeLookupMeta(type):
    metadata_type: Type[MetadataType]


class MetadataTypeLookup(metaclass=MetadataTypeLookupMeta):
    _lookup_dict: Optional[Dict[str, MetadataType]]

    def __init__(self, session: Session, domain_uuid: UUID, entity_type: str):
        self.session = session
        self.domain_uuid = domain_uuid
        self.entity_type = entity_type
        self._lookup_dict = None

    @property
    def lookup_dict(self) -> Dict[str, MetadataType]:
        if self._lookup_dict is None:
            metadata_type_dict = self._lookup_dict = dict(
                (metadata_type.key, metadata_type) for metadata_type in self.lookup_list
            )
            return metadata_type_dict
        else:
            return self._lookup_dict

    @property
    def lookup_list(self) -> List[MetadataType]:
        entity_type_metadata = self._entity_lookup
        if self.entity_type not in entity_type_metadata:
            entity_type_metadata[self.entity_type] = self._fetch_list()
        return entity_type_metadata[self.entity_type]

    @property
    def _entity_lookup(self) -> Dict[str, List[MetadataType]]:
        metadata = self.session.info.setdefault(DRIVR_METADATA_CONTEXT_KEY, {})
        domain_metadata = metadata.setdefault(self.domain_uuid, {})
        entity_type_metadata = domain_metadata.setdefault(DRIVR_METADATA_ENTITY_TYPE_KEY, {})
        return entity_type_metadata

    def _fetch_list(self) -> List[MetadataType]:
        metadata_type = self.__class__.metadata_type
        return (
            self.session.query(metadata_type)
            .filter(and_(metadata_type.domain_uuid == self.domain_uuid, metadata_type.entity_type == self.entity_type))
            .all()
        )
