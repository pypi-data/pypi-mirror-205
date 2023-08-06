from abc import ABC, abstractproperty
from typing import Optional

from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.lookup import MetadataTypeLookup
from xcnt.drivr.metadata_client.search.parser.metadata_base_lookup_parser_mixin import MetadataBaseLookupParserMixin


class KeyedLookupParserMixin(ABC, MetadataBaseLookupParserMixin):
    @abstractproperty
    def entity_type(self) -> str:
        pass

    @property
    def session(self) -> Optional[Session]:
        return self.parse_context.get("session", None)

    @property
    def _lookup(self) -> MetadataTypeLookup:
        assert self.domain_uuid is not None
        return MetadataTypeLookup(session=self.session, domain_uuid=self.domain_uuid, entity_type=self.entity_type)
