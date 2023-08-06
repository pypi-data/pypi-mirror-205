from typing import Any, Dict

from xcnt.sqlalchemy.search.apispec.fields import OpenAPIConverterPlugin

from xcnt.drivr.metadata_client.search import MetadataField


class MetadataFieldOpenAPIConverterPlugin(OpenAPIConverterPlugin[MetadataField]):
    @classmethod
    def supports(cls, entity: Any) -> bool:
        return isinstance(entity, MetadataField)

    def to_openapi(self) -> Dict[str, Any]:
        return {"type": "object", "additionalProperties": {"type": "object", "additionalProperties": True}}
