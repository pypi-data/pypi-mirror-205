from typing import Optional

from xcnt.sqlalchemy.search import fields

from xcnt.drivr.metadata_client.model.metadata_type import MetadataType


class MetadataItem(fields.BaseField):
    def __init__(
        self, metadata_type: MetadataType, attribute_name: Optional[str] = None, description: Optional[str] = None
    ):
        self.metadata_type = metadata_type
        super().__init__(attribute_name=attribute_name, description=description)
