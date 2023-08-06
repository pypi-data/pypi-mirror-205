from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.test.conftest import UserMetadataValue, UserMetadataValueLookup


def test_user_metadata_table_names():
    assert UserMetadataValue.__tablename__ == "user_metadata_value"
    assert UserMetadataValueLookup.__tablename__ == "user_metadata_value_lookup"


def test_metadata_value_query_by_entity_type(session):
    session.query(UserMetadataValueLookup._current_type == DataTypeEnum.STRING).all()
