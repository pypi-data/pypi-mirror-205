from uuid import uuid4

import pytest

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.event import MetadataTypeCreated, MetadataTypeDeleted
from xcnt.drivr.metadata_client.event.metadata_type_events import BaseEvent


@pytest.fixture(autouse=True, scope="session")
def patch_for_entity_types():
    original_selected_entity_types = BaseEvent.selected_entity_types
    BaseEvent.selected_entity_types = ["User", "Organization", "Component"]
    yield BaseEvent.selected_entity_types
    BaseEvent.selected_entity_types = original_selected_entity_types


class CreatedTestEvent(MetadataTypeCreated):
    pass


class DeletedTestEvent(MetadataTypeDeleted):
    pass


@pytest.fixture
def metadata_for_user() -> CreatedTestEvent:
    return CreatedTestEvent(uuid4(), data_type=DataTypeEnum.STRING, entity_type="User")


@pytest.fixture
def metadata_for_organization() -> CreatedTestEvent:
    return CreatedTestEvent(uuid4(), data_type=DataTypeEnum.TIMESTAMP, entity_type="Organization")


@pytest.fixture
def metadata_for_component() -> CreatedTestEvent:
    return CreatedTestEvent(uuid4(), data_type=DataTypeEnum.UUID, entity_type="Component")


@pytest.fixture
def metadata_for_system() -> CreatedTestEvent:
    return CreatedTestEvent(uuid4(), data_type=DataTypeEnum.BOOLEAN, entity_type="System")


@pytest.fixture
def metadata_for_component_model() -> CreatedTestEvent:
    return CreatedTestEvent(uuid4(), data_type=DataTypeEnum.UUID, entity_type="ComponentModel")
