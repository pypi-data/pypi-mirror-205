from typing import Dict, List, Mapping, Type, Union
from uuid import UUID

from sqlalchemy.orm import Session
from webargs import fields

from xcnt.drivr.metadata_client.event.metadata_type_events import BaseEvent
from xcnt.drivr.metadata_client.lookup import MetadataTypeLookup
from xcnt.drivr.metadata_client.model import MetadataType


class WebArgsBuilder:
    def __init__(self, entity_type: str):
        self.entity_type = entity_type

    def fields_for(self, domain_uuid: UUID) -> Mapping[str, Union[type, fields.Field]]:
        metadata_fields = self._metadata_types_for(domain_uuid)
        filters: Dict[str, fields.Field] = {}
        for metadata_field in metadata_fields:
            filters[metadata_field.key] = self.field_for(metadata_field)
        return filters

    def field_for(self, metadata_field: MetadataType) -> fields.Field:
        return metadata_field.to_webargs_field(is_patch=True)

    def _metadata_types_for(self, domain_uuid: UUID) -> List[MetadataType]:
        lookup = MetadataTypeLookup(self.session, domain_uuid, self.entity_type)
        return lookup.lookup_list

    @property
    def session(self) -> Session:
        return BaseEvent.session

    @property
    def sqlalchemy_model(self) -> Type[MetadataType]:
        return BaseEvent.sqlalchemy_model
