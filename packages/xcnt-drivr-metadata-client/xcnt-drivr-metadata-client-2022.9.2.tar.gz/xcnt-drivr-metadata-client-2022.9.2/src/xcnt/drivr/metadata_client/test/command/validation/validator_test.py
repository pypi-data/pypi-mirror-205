from datetime import datetime, timezone

import pytest
from xcnt.cqrs.command import ValidationError

from xcnt.drivr.metadata_client.test.command.conftest import UserCommand


def test_validation_unique(factories, user, birth_date_metadata_type, session):
    other_user = factories.User(domain_uuid=user.domain_uuid)
    birth_date_metadata_type.unique = True
    session.flush()
    other_user.meta.birth_date = datetime(1994, 11, 27).replace(tzinfo=timezone.utc)
    user.meta.birth_date = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    session.flush()

    command = UserCommand(
        user.uuid,
        domain_uuid=user.domain_uuid,
        metadata={"birth_date": datetime(1994, 11, 27).replace(tzinfo=timezone.utc)},
    )
    with pytest.raises(ValidationError):
        command.execute()


def test_validation_unique_success(factories, user, birth_date_metadata_type, session):
    other_user = factories.User(domain_uuid=user.domain_uuid)
    other_user.meta.birth_date = datetime(1994, 11, 27).replace(tzinfo=timezone.utc)
    birth_date_metadata_type.unique = True
    session.flush()
    user.meta.birth_date = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    session.flush()

    command = UserCommand(
        user.uuid,
        domain_uuid=user.domain_uuid,
        metadata={"birth_date": datetime(1994, 11, 28).replace(tzinfo=timezone.utc)},
    )
    command.execute()


def test_validation_unique_null(factories, user, birth_date_metadata_type, session):
    other_user = factories.User(domain_uuid=user.domain_uuid)
    other_user.meta.birth_date = None
    birth_date_metadata_type.unique = True
    session.flush()
    user.meta.birth_date = datetime(1994, 11, 28).replace(tzinfo=timezone.utc)
    session.flush()

    command = UserCommand(user.uuid, domain_uuid=user.domain_uuid, metadata={"birth_date": None})
    command.execute()


def test_validation_unset(factories, user, birth_date_metadata_type, session):
    birth_date = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    command = UserCommand(user.uuid, domain_uuid=user.domain_uuid, metadata={"birth_date": birth_date})
    command.execute()
    session.refresh(user)
    assert user.meta.birth_date == birth_date


def test_validation_mandatory(factories, user, birth_date_metadata_type, session):
    birth_date_metadata_type.mandatory = True
    birth_date = None
    command = UserCommand(user.uuid, domain_uuid=user.domain_uuid, metadata={"birth_date": birth_date})
    with pytest.raises(ValidationError):
        command.execute()


def test_validation_non_mandatory(factories, user, birth_date_metadata_type, session):
    birth_date_metadata_type.mandatory = False
    birth_date = None
    command = UserCommand(user.uuid, domain_uuid=user.domain_uuid, metadata={"birth_date": birth_date})
    command.execute()
    session.refresh(user)
    assert user.meta.birth_date is None


def test_validation_mandatory_and_unique(factories, user, birth_date_metadata_type, session):
    other_user = factories.User(domain_uuid=user.domain_uuid)
    other_user.meta.birth_date = None
    birth_date_metadata_type.unique = True
    birth_date_metadata_type.mandatory = True
    session.flush()
    user.meta.birth_date = datetime(1994, 11, 28).replace(tzinfo=timezone.utc)
    session.flush()

    command = UserCommand(user.uuid, domain_uuid=user.domain_uuid, metadata={"birth_date": None})
    with pytest.raises(ValidationError):
        command.execute()


def test_validation_type_conversion(factories, user, birth_date_metadata_type, session):
    birth_date = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    command = UserCommand(user.uuid, domain_uuid=user.domain_uuid, metadata={"birth_date": birth_date.isoformat()})
    command.execute()
    session.refresh(user)
    assert user.meta.birth_date == birth_date


def test_validation_type_conversion_error(factories, user, birth_date_metadata_type, session):
    command = UserCommand(
        user.uuid,
        domain_uuid=user.domain_uuid,
        metadata={"birth_date": "Firth circle of the moon then venus stands in the star sign of kopernikus"},
    )
    with pytest.raises(ValidationError):
        command.execute()
