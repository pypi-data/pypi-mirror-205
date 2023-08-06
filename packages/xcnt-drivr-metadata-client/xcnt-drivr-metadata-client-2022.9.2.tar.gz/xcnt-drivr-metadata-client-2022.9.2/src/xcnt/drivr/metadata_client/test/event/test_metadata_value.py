from datetime import datetime, timezone
from uuid import uuid4

import pytest

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.test.conftest import User


@pytest.fixture
def weight_metadata_type(user, factories):
    return factories.MetadataType(
        key="weight",
        domain_uuid=user.domain_uuid,
        data_type=DataTypeEnum.FLOAT,
        entity_type="User",
    )


@pytest.fixture
def name_metadata_type(user, factories):
    return factories.MetadataType(
        key="name", domain_uuid=user.domain_uuid, data_type=DataTypeEnum.STRING, entity_type="User"
    )


@pytest.fixture
def authorized_metadata_type(user, factories):
    return factories.MetadataType(
        key="is_authorized",
        domain_uuid=user.domain_uuid,
        data_type=DataTypeEnum.BOOLEAN,
        entity_type="User",
    )


"""
@pytest.fixture
def doc_metadata_type(user, factories):
    return factories.MetadataType(
        key="identity_doc",
        domain_uuid=user.domain_uuid,
        data_type=DataTypeEnum.DOCUMENT,
        entity_type="User",
    )
"""


@pytest.fixture
def age_metadata_type(user, factories):
    return factories.MetadataType(
        key="age", domain_uuid=user.domain_uuid, data_type=DataTypeEnum.INTEGER, entity_type="User"
    )


"""
@pytest.fixture
def profile_metadata_type(user, factories):
    return factories.MetadataType(
        key="profile_pic", domain_uuid=user.domain_uuid, data_type=DataTypeEnum.IMAGE, entity_type="User"
    )
"""


@pytest.fixture
def uuid_metadata_type(user, factories):
    return factories.MetadataType(
        key="sibling_id", domain_uuid=user.domain_uuid, data_type=DataTypeEnum.UUID, entity_type="User"
    )


def test_metadata_float_value_set_event(user_metadata_value_events, user, weight_metadata_type, event_registry):
    float_set_event = user_metadata_value_events[DataTypeEnum.FLOAT]
    event = float_set_event(user.uuid, metadata_type_uuid=weight_metadata_type.uuid, value=83.8)
    event_registry.handle(event)
    assert user.meta.weight == 83.8


def test_metadata_float_value_set_with_non_existing_user(
    user_metadata_value_events, user, weight_metadata_type, event_registry, session
):
    float_set_event = user_metadata_value_events[DataTypeEnum.FLOAT]
    event = float_set_event(uuid4(), metadata_type_uuid=weight_metadata_type.uuid, value=84.9)
    event_registry.handle(event)
    created_user = session.query(User).filter(User.uuid == event.aggregate_id).first()
    assert created_user is not None
    created_user.domain_uuid = weight_metadata_type.domain_uuid
    assert created_user.meta.weight == 84.9


def test_metadata_float_value_set_event_without_metadata_type(
    user_metadata_value_events, user, event_registry, session
):
    float_set_event = user_metadata_value_events[DataTypeEnum.FLOAT]
    event = float_set_event(user.uuid, metadata_type_uuid=uuid4(), value=57.0)
    event_registry.handle(event)
    session.refresh(user)
    assert len(user.metadata_values) == 1
    assert user.metadata_values[0].metadata_value.value_float == 57.0
    assert user.metadata_values[0].metadata_type_uuid == event.metadata_type_uuid


def test_metadata_string_value_set_event(user_metadata_value_events, user, name_metadata_type, event_registry):
    value = "Alexa"
    string_set_event = user_metadata_value_events[DataTypeEnum.STRING]
    event = string_set_event(user.uuid, metadata_type_uuid=name_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.name == value


def test_metadata_multiple_values_set(
    user_metadata_value_events, user, weight_metadata_type, name_metadata_type, event_registry, session
):
    float_set_event = user_metadata_value_events[DataTypeEnum.FLOAT]
    event_1 = float_set_event(user.uuid, metadata_type_uuid=weight_metadata_type.uuid, value=57.0)
    string_set_event = user_metadata_value_events[DataTypeEnum.STRING]
    value = "Alexa"
    event_2 = string_set_event(user.uuid, metadata_type_uuid=name_metadata_type.uuid, value=value)
    event_registry.handle_batch([event_1, event_2])
    session.commit()
    session.refresh(user)
    assert user.meta.name == value
    assert user.meta.weight == 57.0
    assert len(user.metadata_values) == 2


def test_metadata_float_and_string_set(
    user_metadata_value_events, user, name_metadata_type, weight_metadata_type, event_registry
):
    float_set_event = user_metadata_value_events[DataTypeEnum.FLOAT]
    string_set_event = user_metadata_value_events[DataTypeEnum.STRING]

    event_string = string_set_event(user.uuid, metadata_type_uuid=name_metadata_type.uuid, value="Alexa")
    event_float = float_set_event(uuid4(), metadata_type_uuid=weight_metadata_type.uuid, value=84.9)

    event_registry.handle_batch([event_string, event_float])


def test_metadata_boolean_value_set_event(user_metadata_value_events, user, authorized_metadata_type, event_registry):
    value = False
    bool_set_event = user_metadata_value_events[DataTypeEnum.BOOLEAN]
    event = bool_set_event(user.uuid, metadata_type_uuid=authorized_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.is_authorized == value


def test_metadata_timestamp_value_set_event(user_metadata_value_events, user, birth_date_metadata_type, event_registry):
    value = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    timestamp_set_event = user_metadata_value_events[DataTypeEnum.TIMESTAMP]
    event = timestamp_set_event(user.uuid, metadata_type_uuid=birth_date_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.birth_date == value


def test_metadata_timestamp_value_set_without_time_zone(
    user_metadata_value_events, user, birth_date_metadata_type, event_registry
):
    value = datetime(1988, 1, 20, 1, 0, 0)
    timestamp_set_event = user_metadata_value_events[DataTypeEnum.TIMESTAMP]
    event = timestamp_set_event(user.uuid, metadata_type_uuid=birth_date_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.birth_date == value.astimezone(timezone.utc)


def test_metadata_timestamp_value_set_with_timezone(
    user_metadata_value_events, user, birth_date_metadata_type, event_registry
):
    value = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    timestamp_set_event = user_metadata_value_events[DataTypeEnum.TIMESTAMP]
    event = timestamp_set_event(user.uuid, metadata_type_uuid=birth_date_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.birth_date == value


def test_metadata_integer_value_set_event(user_metadata_value_events, user, age_metadata_type, event_registry):
    value = 32
    integer_set_event = user_metadata_value_events[DataTypeEnum.INTEGER]
    event = integer_set_event(user.uuid, metadata_type_uuid=age_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.age == value


#########################################################################
#                                                                       #
#  CAUTION:                                                             #
#  Commented out until document and image are fully supported by DRIVR  #
#                                                                       #
#########################################################################

"""
def test_metadata_image_value_set_event(user_metadata_value_events, user, profile_metadata_type, event_registry):
    value = uuid4()
    image_set_event = user_metadata_value_events[DataTypeEnum.IMAGE]
    event = image_set_event(user.uuid, metadata_type_uuid=profile_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.profile_pic == value


def test_metadata_document_value_set_event(user_metadata_value_events, user, doc_metadata_type, event_registry):
    value = uuid4()
    doc_set_event = user_metadata_value_events[DataTypeEnum.DOCUMENT]
    event = doc_set_event(user.uuid, metadata_type_uuid=doc_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.identity_doc == value
"""


def test_metadata_uuid_value_set_event(user_metadata_value_events, user, uuid_metadata_type, event_registry):
    value = uuid4()
    uuid_set_event = user_metadata_value_events[DataTypeEnum.UUID]
    event = uuid_set_event(user.uuid, metadata_type_uuid=uuid_metadata_type.uuid, value=value)
    event_registry.handle(event)
    assert user.meta.sibling_id == value
