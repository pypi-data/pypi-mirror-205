from __future__ import annotations

from uuid import UUID

from xcnt.cqrs.command import Attribute

from xcnt.drivr.metadata_client.command import MetadataValueCommand
from xcnt.drivr.metadata_client.test.conftest import Session, TestCommand, User


class UserCommand(MetadataValueCommand, TestCommand):
    sqlalchemy_model = User
    session = Session
    metadata_entity_type = "User"

    domain_uuid: Attribute[UUID]

    @property
    def metadata_domain_uuid(self) -> UUID:
        return self.domain_uuid
