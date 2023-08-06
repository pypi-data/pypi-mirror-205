from functools import cached_property
from typing import Any, Dict, List, Type, cast
from uuid import UUID

from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.model.metadata_value import (
    INITIATED_METADATA_VALUE_CLASSES,
    INITIATED_METADATA_VALUE_LOOKUP_CLASSES,
    MetadataValue,
)
from xcnt.drivr.metadata_client.model.metadata_value import MetadataValueLookup as MetadataValueLookupModel


class MetadataValueLookup:
    def __init__(self, session: Session, entity_type: str, entity_uuid: UUID):
        self.session = session
        self.entity_type = entity_type
        self.entity_uuid = entity_uuid

    @property
    def metadata_value_class(self) -> Type[MetadataValue]:
        return INITIATED_METADATA_VALUE_CLASSES[self.entity_type]

    @property
    def metadata_value_lookup_class(self) -> Type[MetadataValueLookupModel]:
        return INITIATED_METADATA_VALUE_LOOKUP_CLASSES[self.entity_type]

    @cached_property
    def values(self) -> Dict[str, Any]:
        return dict(
            (cast(str, metadata_lookup.key), metadata_lookup.value) for metadata_lookup in self._fetch_value_list()
        )

    def _fetch_value_list(self) -> List[MetadataValueLookupModel]:
        return (
            self.session.query(self.metadata_value_lookup_class)
            .filter(self.metadata_value_lookup_class.entity_uuid == self.entity_uuid)
            .all()
        )
