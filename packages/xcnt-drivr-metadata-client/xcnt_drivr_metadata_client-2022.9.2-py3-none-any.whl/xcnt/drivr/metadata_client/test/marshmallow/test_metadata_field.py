from datetime import datetime, timezone

import pytest
from marshmallow import Schema

from xcnt.drivr.metadata_client.marshmallow import MetadataField
from xcnt.drivr.metadata_client.test.conftest import Session


class UserSchema(Schema):
    meta = MetadataField(entity_type="User", session=Session, domain_uuid_receiver=lambda obj: obj.domain_uuid)


class UserSchemaWithoutSession(Schema):
    meta = MetadataField(entity_type="User", domain_uuid_receiver=lambda obj: obj.domain_uuid)


class UserSchemaWithoutDomainUUID(Schema):
    meta = MetadataField(entity_type="User", session=Session)


class UserSchemaWithNoneDomain(Schema):
    meta = MetadataField(entity_type="User", session=Session, domain_uuid_receiver=lambda obj: None)


def test_schema_dump(user, birth_date_metadata_type):
    birth_date = datetime(1994, 11, 27)
    user.meta.birth_date = birth_date
    user_data = UserSchema().dump(user)
    assert user_data["meta"]["birth_date"] == birth_date.replace(tzinfo=timezone.utc).isoformat()


def test_schema_dump_without_entry(user, birth_date_metadata_type):
    birth_date = None
    user.meta.birth_date = birth_date
    user_data = UserSchema().dump(user)
    assert user_data["meta"]["birth_date"] is None


def test_schema_dump_with_other_domain(factories, user, birth_date_metadata_type):
    other_user = factories.User()
    user_data = UserSchema().dump(other_user)
    assert user_data["meta"] == {}


def test_schema_dump_with_injected_session(user, birth_date_metadata_type):
    birth_date = datetime(1994, 11, 27)
    user.meta.birth_date = birth_date
    user_data = UserSchemaWithoutSession(context=dict(session=Session)).dump(user)
    assert user_data["meta"]["birth_date"] == birth_date.replace(tzinfo=timezone.utc).isoformat()


def test_schema_dump_with_injected_domain_uuid(user, birth_date_metadata_type):
    birth_date = datetime(1994, 11, 27)
    user.meta.birth_date = birth_date
    user_data = UserSchemaWithoutDomainUUID(context=dict(domain_uuid=user.domain_uuid)).dump(user)
    assert user_data["meta"]["birth_date"] == birth_date.replace(tzinfo=timezone.utc).isoformat()


def test_schema_dump_without_injected_domain_uuid_or_reciever(user, birth_date_metadata_type):
    birth_date = datetime(1994, 11, 27)
    user.meta.birth_date = birth_date
    with pytest.raises(ValueError):
        UserSchemaWithoutDomainUUID().dump(user)


def test_schema_dump_with_none_domain_in_receiver(user, birth_date_metadata_type):
    birth_date = datetime(1994, 11, 27)
    user.meta.birth_date = birth_date
    user_data = UserSchemaWithNoneDomain().dump(user)
    assert user_data["meta"] == {}


def test_schema_dump_with_none_domain(user, birth_date_metadata_type):
    birth_date = datetime(1994, 11, 27)
    user.meta.birth_date = birth_date
    user_data = UserSchemaWithoutDomainUUID(context=dict(domain_uuid=None)).dump(user)
    assert user_data["meta"] == {}


def test_schema_load(birth_date_metadata_type):
    birth_date = datetime(1988, 1, 20)
    data = {"meta": {"something_else": "fjasdjfdsa", "birth_date": birth_date.isoformat()}}
    loaded_data = UserSchema(context=dict(domain_uuid=birth_date_metadata_type.domain_uuid)).load(data)
    assert loaded_data["meta"] == {"birth_date": birth_date}
