from typing import Any, Dict

from xcnt.sqlalchemy.search import fields
from xcnt.sqlalchemy.search.apispec.fields import OpenAPIConverterPlugin

from xcnt.drivr.metadata_client.search import MetadataKeyValueStoreField
from xcnt.drivr.metadata_client.search.metadata_key_value_store_field import MetadataGenericValueField

OPENAPI_DEFINITION = {"type": "object", "properties": {"type": "object", "properties": {"key": {}}}}


class MetadataKeyValueStoreFieldOpenAPIConverterPlugin(OpenAPIConverterPlugin[MetadataKeyValueStoreField]):
    @classmethod
    def supports(cls, entity: Any) -> bool:
        return isinstance(entity, MetadataKeyValueStoreField)

    def to_openapi(self) -> Dict[str, Any]:
        if MetadataKeyValueStoreField not in self.converter.resolved_schemas:
            self._generate_key_value_store_field_schema()
        return self.converter.build_schema_reference(MetadataKeyValueStoreField.__name__)

    def _generate_key_value_store_field_schema(self) -> None:
        resource_schema = {
            "type": "object",
            "properties": {
                "key": self.converter.build_field(fields.String()),
                "value": self._generate_metadata_generic_value_field_reference(),
            },
        }
        self.converter.register_resource(MetadataKeyValueStoreField.__name__, resource_schema)
        self.converter.resolved_schemas[MetadataKeyValueStoreField] = resource_schema

    def _generate_metadata_generic_value_field_reference(self) -> Dict[str, Any]:
        value_field_name = MetadataGenericValueField.__name__

        if MetadataGenericValueField not in self.converter.resolved_schemas:
            properties = {
                key: self.converter.build_field(field) for key, field in MetadataGenericValueField._fields.items()
            }
            resource_schema = {
                "type": "object",
                "properties": {
                    "type": "object",
                    "properties": properties,
                },
            }
            self.converter.register_resource(value_field_name, resource_schema)
            self.converter.resolved_schemas[MetadataGenericValueField] = resource_schema
        return self.converter.build_schema_reference(value_field_name)
