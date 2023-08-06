from uuid import uuid4

import factory

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.test.conftest import MetadataType
from xcnt.drivr.metadata_client.test.factories.base import BaseFactory


class MetadataTypeFactory(BaseFactory):
    class Meta:
        model = MetadataType

    domain_uuid = factory.LazyFunction(uuid4)
    entity_type = factory.Iterator(
        ["System", "User", "Organization", "Address", "Component", "ComponentModel", "Location"]
    )
    data_type = DataTypeEnum.STRING
    key = factory.Sequence(lambda i: f"key-{i}")
    mandatory = False
    unique = False
    description = factory.Sequence(lambda i: f"description-{i}")
