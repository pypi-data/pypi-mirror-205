from typing import Any, Dict, Optional

from xcnt.sqlalchemy.search.api_gateway_crd.argument_collection_representation import ArgumentCollectionRepresentation
from xcnt.sqlalchemy.search.api_gateway_crd.base_resource_converter import new_template
from xcnt.sqlalchemy.search.api_gateway_crd.fields import APIGatewayConverterPlugin
from xcnt.sqlalchemy.search.api_gateway_crd.resource_generator import ResourceGenerator

from xcnt.drivr.metadata_client.search.metadata_key_value_store_field import (
    MetadataGenericValueField,
    MetadataKeyValueStoreField,
)

METADATA_KEY_VALUE_STORE_NAME = "metadata-key-value-store-query-field"
COLLECTION_ARGS = {
    "key": {"in": "query", "type": {"argumentCollectionRef": "string-query-field", "list": False, "object": True}},
    "value": {
        "in": "query",
        "type": {
            "argumentCollectionRef": MetadataGenericValueField.Meta.apigateway_name,
            "list": False,
            "object": True,
        },
    },
}


class MetadataKeyValueStoreFieldAPIGatewayCRDConverterPlugin(APIGatewayConverterPlugin[MetadataKeyValueStoreField]):
    @classmethod
    def supports(cls, entity: Any) -> bool:
        return isinstance(entity, MetadataKeyValueStoreField)

    def to_api_gateway_part(self) -> Optional[Dict[str, Any]]:
        self._ensure_argument_collections()

        return {"type": {"argumentCollectionRef": METADATA_KEY_VALUE_STORE_NAME, "list": False, "object": True}}

    def _ensure_argument_collections(self) -> None:
        self._ensure_key_value_store_argument_collection()
        self._ensure_value_store_argument_collection()

    def _ensure_value_store_argument_collection(self) -> None:
        resource_generator = ResourceGenerator(MetadataGenericValueField, self.generator)
        resource_generator.generate_if_not_present()

    def _ensure_key_value_store_argument_collection(self) -> None:
        collection = self.generator.collection_for(self.item.__class__)

        if collection is None:
            spec = new_template(METADATA_KEY_VALUE_STORE_NAME)
            spec["spec"]["arguments"] = COLLECTION_ARGS
            collection = ArgumentCollectionRepresentation(
                name=METADATA_KEY_VALUE_STORE_NAME,
                resource=self.item.__class__,
                spec={**spec},
            )
            self.generator.add_argument_collection(collection)
