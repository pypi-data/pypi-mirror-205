import factory

from xcnt.drivr.metadata_client.test.conftest import Session


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_session = Session
