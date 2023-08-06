from uuid import uuid4

import factory

from xcnt.drivr.metadata_client.test.conftest import User
from xcnt.drivr.metadata_client.test.factories.base import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = User

    domain_uuid = factory.LazyFunction(uuid4)
