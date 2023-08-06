import os

import pytest
from apscheduler.util import asbool
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import Column, create_engine, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from xcnt.cqrs.command import Command
from xcnt.cqrs.event import Event, Registry

from xcnt.drivr.metadata_client.configuration import (
    metadata_type_model_for,
    metadata_value_model_for,
    register_metadata_events_for,
)
from xcnt.drivr.metadata_client.enum import DataTypeEnum, MetadataValueFeatureEnum
from xcnt.drivr.metadata_client.event import METADATA_VALUE_TYPE_BY_DATA_TYPE_ENUM
from xcnt.drivr.metadata_client.model import MetadataField

Base = declarative_base()
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
MetadataType = metadata_type_model_for(Base, Session)
test_registry = Registry()


class User(Base):  # type: ignore
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    domain_uuid = Column(UUID(as_uuid=True), nullable=True)
    meta = MetadataField(entity_type="User", domain_uuid="domain_uuid")


UserMetadataValue, UserMetadataValueLookup = metadata_value_model_for(
    Base,
    "User",
    User,
    features=(
        MetadataValueFeatureEnum.ENABLE_STRING_INDEX_BY_SHA_HASH,
        MetadataValueFeatureEnum.ENABLE_GIN_INDEX_FOR_LIKE,
    ),
)
USER_METADATA_VALUE_EVENTS = register_metadata_events_for(test_registry, UserMetadataValueLookup, "User", Session)


class TestCommand(Command):
    def _emit(self, event: Event):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    @property
    def event_registry(self) -> Registry:
        return test_registry


@pytest.fixture
def factories(session, engine):
    from xcnt.drivr.metadata_client.test import factories

    Base.metadata.bind = engine

    return factories


@pytest.fixture
def user(factories):
    return factories.User()


@pytest.fixture
def domain_uuid(user) -> UUID:
    return user.domain_uuid


@pytest.fixture
def customer_number_metadata_type(domain_uuid, factories):
    return factories.MetadataType(
        key="customer_number",
        domain_uuid=domain_uuid,
        data_type=DataTypeEnum.STRING,
        entity_type="User",
    )


@pytest.fixture
def birth_date_metadata_type(user, factories):
    return factories.MetadataType(
        key="birth_date",
        domain_uuid=user.domain_uuid,
        data_type=DataTypeEnum.TIMESTAMP,
        entity_type="User",
    )


@pytest.fixture
def special_metadata_type(domain_uuid, factories):
    return factories.MetadataType(
        key="special",
        domain_uuid=domain_uuid,
        data_type=DataTypeEnum.STRING,
        entity_type="User",
    )


@pytest.fixture
def really_special_metadata_type(domain_uuid, factories):
    return factories.MetadataType(
        key="really_special",
        domain_uuid=domain_uuid,
        data_type=DataTypeEnum.STRING,
        entity_type="User",
    )


@pytest.fixture
def event_registry():
    return test_registry


@pytest.fixture
def user_metadata_value_events():
    return dict(
        (data_type, USER_METADATA_VALUE_EVENTS[value_type_name])
        for data_type, value_type_name in METADATA_VALUE_TYPE_BY_DATA_TYPE_ENUM.items()
    )


@pytest.fixture(scope="session")
def engine():
    try:
        load_dotenv(find_dotenv())
    except OSError:
        pass

    engine = create_engine(os.getenv("SQLALCHEMY_URL"), echo=asbool(os.getenv("SQLALCHEMY_ECHO", "False")))

    # This call is not required for unit tests, since they all share the same table structure and the session fixture
    # ensures that the tables are empty before tests are run.
    # Dropping all and Recreating all takes > 30 seconds to run when re-running pytest in your IDE. The drop_all call
    # is left here as an example to clean up, if necessary, i.e, you develop a new table structure.
    # Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    Session.configure(bind=engine)
    Base.metadata.bind = engine
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine):
    Session.rollback()
    engine.execute(";".join(f"DELETE FROM {table.name}" for table in reversed(Base.metadata.sorted_tables)))
    yield Session
    Session.rollback()
    Session.close_all()
