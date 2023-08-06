from typing import Any, Dict, Type
from uuid import UUID

from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.lookup.metadata_type_lookup import MetadataTypeLookup
from xcnt.drivr.metadata_client.lookup.metadata_value_lookup import MetadataValueLookup
from xcnt.drivr.metadata_client.model.metadata_type import MetadataType
from xcnt.drivr.metadata_client.model.metadata_value import MetadataValue
from xcnt.drivr.metadata_client.model.metadata_value import MetadataValueLookup as MetadataValueLookupModel


class MetadataLookup:
    def __init__(self, session: Session, entity_type: str, entity_uuid: UUID, domain_uuid: UUID):
        self._value_lookup = MetadataValueLookup(
            session=session,
            entity_type=entity_type,
            entity_uuid=entity_uuid,
        )
        self._type_lookup = MetadataTypeLookup(
            session=session,
            entity_type=entity_type,
            domain_uuid=domain_uuid,
        )

    @property
    def metadata_value_class(self) -> Type[MetadataValue]:
        return self._value_lookup.metadata_value_class

    @property
    def metadata_value_lookup_class(self) -> Type[MetadataValueLookupModel]:
        return self._value_lookup.metadata_value_lookup_class

    @property
    def values(self) -> Dict[str, Any]:
        return self._value_lookup.values

    @property
    def types(self) -> Dict[str, MetadataType]:
        return self._type_lookup.lookup_dict
