from typing import Any, Dict, Optional

from xcnt.sqlalchemy.search.api_gateway_crd.fields import APIGatewayConverterPlugin

from xcnt.drivr.metadata_client.search import MetadataField


class MetadataFieldAPIGatewayCRDConverterPlugin(APIGatewayConverterPlugin[MetadataField]):
    @classmethod
    def supports(cls, entity: Any) -> bool:
        return isinstance(entity, MetadataField)

    def to_api_gateway_part(self) -> Optional[Dict[str, Any]]:
        return None
