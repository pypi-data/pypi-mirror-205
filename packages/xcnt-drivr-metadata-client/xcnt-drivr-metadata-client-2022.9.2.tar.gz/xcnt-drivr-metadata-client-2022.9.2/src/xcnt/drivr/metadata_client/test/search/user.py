from xcnt.sqlalchemy.search import Resource, fields

from xcnt.drivr.metadata_client.search import MetadataField, MetadataKeyValueStoreField
from xcnt.drivr.metadata_client.test.conftest import User


class UserQuery(Resource):
    class Meta:
        model = User

    domain_uuid = fields.UUID()

    meta = MetadataField()
    metadata_key_value_store = MetadataKeyValueStoreField()
