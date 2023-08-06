from xcnt.sqlalchemy.search import Resource, fields

from xcnt.drivr.metadata_client.model.metadata_value import MetadataValue
from xcnt.drivr.metadata_client.search.metadata_field import MetadataFieldBase


class MetadataGenericValueField(Resource):
    class Meta:
        model = MetadataValue
        apigateway_name = "metadata-generic-value-query-field"
        apigateway_doc = "Filter by the metadata value"

    boolean = fields.Boolean(table_column_name="value_boolean", description="Filter by boolean metadata value")
    float = fields.Float(table_column_name="value_float", description="Filter by float metadata value")
    integer = fields.Integer(table_column_name="value_integer", description="Filter by integer metadata value")
    string = fields.Sha256String(table_column_name="value_string", description="Filter by string metadata value")
    uuid = fields.UUID(table_column_name="value_uuid", description="Filter by uuid metadata value")
    timestamp = fields.DateTime(table_column_name="value_timestamp", description="Filter by timestamp metadata value")


class MetadataKeyValueStoreField(MetadataFieldBase):
    ...
