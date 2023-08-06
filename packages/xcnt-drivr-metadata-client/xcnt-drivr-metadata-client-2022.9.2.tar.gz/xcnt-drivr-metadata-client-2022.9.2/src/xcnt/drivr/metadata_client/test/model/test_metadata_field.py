from datetime import datetime, timezone

import pytest

from xcnt.drivr.metadata_client.lookup import MetadataTypeLookup
from xcnt.drivr.metadata_client.test.conftest import User


def test_user_metadata_birth_date(session, user, birth_date_metadata_type, factories):
    user.meta.birth_date = datetime(1994, 11, 27).replace(tzinfo=timezone.utc)
    other_user = factories.User(domain_uuid=user.domain_uuid)
    other_user.meta.birth_date = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    session.commit()

    loaded_user = session.query(User).filter(User.uuid == user.uuid).first()
    assert loaded_user.meta.birth_date == datetime(1994, 11, 27).replace(tzinfo=timezone.utc)


def test_user_in_other_domain_metadata_error(session, user, birth_date_metadata_type, factories):
    other_user = factories.User()
    with pytest.raises(AttributeError):
        other_user.meta.birth_date == datetime(1988, 1, 20).replace(tzinfo=timezone.utc)


def test_session_stored(session, user, birth_date_metadata_type):
    user.meta.birth_date
    user_metadata = session.info["drivr_metadata"][user.domain_uuid]["entity_types"]["User"]
    assert birth_date_metadata_type.uuid in [item.uuid for item in user_metadata]


def test_session_metadata_cached(session, user, birth_date_metadata_type, mocker, factories):
    other_user = factories.User(domain_uuid=user.domain_uuid)
    spy = mocker.spy(MetadataTypeLookup, "_fetch_list")
    user.meta.birth_date
    other_user.meta.birth_date
    spy.assert_called_once()


@pytest.mark.parametrize("callback_function", ["commit", "rollback"])
def test_session_released_on(session, user, birth_date_metadata_type, callback_function):
    user.meta.birth_date
    session_function = getattr(session, callback_function)
    session_function()
    assert not session.info.get("drivr_metadata", {})
