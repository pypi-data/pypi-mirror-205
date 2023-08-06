from abc import abstractproperty
from typing import Any, Dict, Iterable
from uuid import UUID

from sqlalchemy.orm import Session
from xcnt.cqrs.command import Attribute
from xcnt.cqrs.command.command import Command, CommandMeta
from xcnt.cqrs.event import Event

from xcnt.drivr.metadata_client.command.metadata_execution import MetadataExecution
from xcnt.drivr.metadata_client.command.validation import MetadataValidator


class MetadataValueCommandMeta(CommandMeta):
    metadata_entity_type: str


class MetadataValueCommand(Command, metaclass=MetadataValueCommandMeta):
    aggregate_id: UUID
    metadata: Attribute[Dict[str, Any]]
    metadata_entity_type: str

    @abstractproperty
    def metadata_domain_uuid(self) -> UUID:
        pass

    @abstractproperty
    def session(self) -> Session:
        pass

    @property
    def events(self) -> Iterable[Event]:
        yield from super().events  # type: ignore
        yield from MetadataExecution(self).generate_events()

    @property
    def _validation_instance(self) -> MetadataValidator:
        return MetadataValidator(command=self)
