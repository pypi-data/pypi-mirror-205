from datetime import datetime, timezone

import pytest
from marshmallow import Schema, ValidationError

from xcnt.drivr.metadata_client.marshmallow import MetadataField
from xcnt.drivr.metadata_client.marshmallow.metadata_key_value_store import MetadataKeyValueStore
from xcnt.drivr.metadata_client.test.conftest import Session


@MetadataKeyValueStore()
class UserSchema(Schema):
    meta = MetadataField(entity_type="User", session=Session, domain_uuid_receiver=lambda obj: obj.domain_uuid)


@MetadataKeyValueStore(is_loader=True)
class UserLoaderSchema(Schema):
    meta = MetadataField(entity_type="User", session=Session, domain_uuid_receiver=lambda obj: obj.domain_uuid)


def test_schema_dump(user, birth_date_metadata_type):
    birth_date = datetime(1994, 11, 27)
    user.meta.birth_date = birth_date
    user_data = UserSchema().dump(user)
    utc_birth_date = birth_date.replace(tzinfo=timezone.utc).isoformat()
    assert user_data["meta"]["birth_date"] == utc_birth_date
    assert len(user_data["metadata_key_value_store"]) == 1
    assert user_data["metadata_key_value_store"][0]["key"] == "birth_date"
    assert user_data["metadata_key_value_store"][0]["value"] == utc_birth_date


def test_schema_dump_without_entry(user, birth_date_metadata_type):
    birth_date = None
    user.meta.birth_date = birth_date
    user_data = UserSchema().dump(user)
    assert user_data["meta"]["birth_date"] is None
    assert len(user_data["metadata_key_value_store"]) == 1
    assert user_data["metadata_key_value_store"][0]["key"] == "birth_date"
    assert user_data["metadata_key_value_store"][0]["value"] is None


def test_schema_dump_with_other_domain(factories, user, birth_date_metadata_type):
    other_user = factories.User()
    user_data = UserSchema().dump(other_user)
    assert user_data["meta"] == {}
    assert user_data["metadata_key_value_store"] == []


def test_schema_load_success(birth_date_metadata_type):
    birth_date = datetime(1988, 1, 20)
    data = {
        "metadata_key_value_store": [
            {"key": "birth_date", "value": {"timestamp": birth_date.isoformat()}},
        ]
    }
    loaded_data = UserLoaderSchema(context=dict(domain_uuid=birth_date_metadata_type.domain_uuid)).load(data)
    assert loaded_data["metadata_key_value_store"] == [
        {"value": {"timestamp": datetime(1988, 1, 20, 0, 0)}, "key": "birth_date"}
    ]


def test_schema_load_fail_undefined_metadata(birth_date_metadata_type):
    birth_date = datetime(1988, 1, 20)
    data = {
        "metadata_key_value_store": [
            {"key": "something_else", "value": {"string": "fjasdjfdsa"}},
            {"key": "birth_date", "value": {"timestamp": birth_date.isoformat()}},
        ]
    }
    with pytest.raises(ValidationError):
        UserLoaderSchema(context=dict(domain_uuid=birth_date_metadata_type.domain_uuid)).load(data)


def test_schema_load_fail_invalid_metadata_store(birth_date_metadata_type):
    data = {"metadata_key_value_store": ["foo"]}
    with pytest.raises(AssertionError):
        UserLoaderSchema(context=dict(domain_uuid=birth_date_metadata_type.domain_uuid)).load(data)


def test_schema_load_fail_missing_key(birth_date_metadata_type):
    data = {"metadata_key_value_store": [{"foo": "bar"}]}
    with pytest.raises(ValidationError):
        UserLoaderSchema(context=dict(domain_uuid=birth_date_metadata_type.domain_uuid)).load(data)
