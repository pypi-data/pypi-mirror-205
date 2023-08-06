from __future__ import annotations

from datetime import datetime, timezone
from functools import partial

import pytest

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.test.command.conftest import UserCommand


@pytest.fixture
def birth_date_metadata_type(birth_date_metadata_type, session):
    birth_date_metadata_type.default_value = datetime(1994, 11, 27).replace(tzinfo=timezone.utc)
    session.flush()
    return birth_date_metadata_type


@pytest.fixture
def user_command(user) -> UserCommand:
    return UserCommand(aggregate_id=user.uuid, domain_uuid=user.domain_uuid)


@pytest.fixture
def birth_date_set_event_factory(user, birth_date_metadata_type, user_metadata_value_events):
    value_event_class = user_metadata_value_events[DataTypeEnum.TIMESTAMP]
    return partial(value_event_class, aggregate_id=user.uuid, metadata_type_uuid=birth_date_metadata_type.uuid)


def test_user_birth_date_default_value_add(
    user_command, birth_date_metadata_type, session, user, event_mocker, birth_date_set_event_factory
):
    user_command.execute()
    session.refresh(user)
    assert user.meta.birth_date == birth_date_metadata_type.default_value
    assert event_mocker.emitted(birth_date_set_event_factory(value=birth_date_metadata_type.default_value))


def test_user_command_birth_date_update(
    user_command, birth_date_metadata_type, event_mocker, session, user, birth_date_set_event_factory
):
    user_birth_date = datetime(1997, 1, 9).replace(tzinfo=timezone.utc)
    user_command.metadata = {"birth_date": user_birth_date}
    user_command.execute()
    session.refresh(user)
    assert user.meta.birth_date == user_birth_date
    assert event_mocker.emitted(birth_date_set_event_factory(value=user_birth_date))


def test_update_of_existing_birth_date(
    user_command, birth_date_metadata_type, event_mocker, session, user, birth_date_set_event_factory
):
    user_birth_date = datetime(1994, 11, 27).replace(tzinfo=timezone.utc)
    user.meta.birth_date = user_birth_date
    session.commit()
    session.refresh(user)
    assert user.meta.birth_date == user_birth_date
    user_birth_date = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    user_command.metadata = {"birth_date": user_birth_date}
    user_command.execute()
    session.commit()
    session.refresh(user)
    assert user.meta.birth_date == user_birth_date
    assert event_mocker.emitted(birth_date_set_event_factory(value=user_birth_date))


def test_no_event_emit_on_same_birth_date(
    user_command, birth_date_metadata_type, event_mocker, session, user, birth_date_set_event_factory
):
    user_birth_date = datetime(1994, 11, 27).replace(tzinfo=timezone.utc)
    user.meta.birth_date = user_birth_date
    session.flush()
    user_command.metadata = {"birth_date": user_birth_date}
    user_command.execute()
    assert not event_mocker.emitted(birth_date_set_event_factory(value=user_birth_date))


def test_no_overwrite_of_default(
    user_command, birth_date_metadata_type, event_mocker, session, user, birth_date_set_event_factory
):
    user.meta.birth_date = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    session.flush()
    user_command.metadata = {}
    user_command.execute()
    assert not event_mocker.emitted(birth_date_set_event_factory(value=birth_date_metadata_type.default_value))


def test_no_metadata_set_no_overwrite(birth_date_metadata_type, user, session):
    user_birth_date = datetime(1994, 11, 27).replace(tzinfo=timezone.utc)
    user.meta.birth_date = user_birth_date
    session.commit()
    assert user.meta.birth_date == user_birth_date

    user_command = UserCommand(aggregate_id=user.uuid, domain_uuid=user.domain_uuid)
    user_command.execute()

    session.refresh(user)
    assert user.meta.birth_date == user_birth_date
