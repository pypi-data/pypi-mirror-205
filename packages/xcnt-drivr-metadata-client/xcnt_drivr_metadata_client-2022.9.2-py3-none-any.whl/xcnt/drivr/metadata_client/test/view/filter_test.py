import json
from datetime import datetime, timezone

import pytest

from xcnt.drivr.metadata_client.view import filter_for


@pytest.fixture
def user(user, session, birth_date_metadata_type):
    user.meta.birth_date = datetime(1994, 11, 27).replace(tzinfo=timezone.utc)
    session.commit()
    return user


@pytest.fixture
def other_user(user, session, factories):
    other_user = factories.User(domain_uuid=user.domain_uuid)
    other_user.meta.birth_date = datetime(1988, 1, 20).replace(tzinfo=timezone.utc)
    session.commit()
    return other_user


@pytest.mark.parametrize("as_json", [True, False])
@pytest.mark.parametrize("with_list", [True, False])
@pytest.mark.parametrize(
    "meta_kwargs", [{}, {"metadata_field_name": "metadata"}, {"metadata_field_name": "something_else"}]
)
def test_user_metadata_birth_date(session, user, other_user, as_json, with_list, meta_kwargs):
    birth_date = user.meta.birth_date.isoformat()
    meta_query_dict = {"birth_date": [birth_date] if with_list else birth_date}
    metadata_field = meta_kwargs.get("metadata_field_name", "metadata")
    meta_query = {metadata_field: json.dumps(meta_query_dict) if as_json else meta_query_dict}

    meta_filter = filter_for(user.__class__, domain_uuid=user.domain_uuid, **meta_kwargs)
    query = session.query(user.__class__).filter(meta_filter(meta_query))
    assert query.count() == 1
    retrieved_user = query.first()
    assert retrieved_user.uuid == user.uuid


def test_user_without_meta(session, user, other_user):
    meta_filter = filter_for(user.__class__, domain_uuid=user.domain_uuid)
    query = session.query(user.__class__).filter(meta_filter({}))
    assert query.count() == 2
