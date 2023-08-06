from typing import Type

from xcnt.sqlalchemy.search import fields

from xcnt.drivr.metadata_client.model.metadata_type import MetadataType


class MetadataTypeKey(fields.ConcreteBase):
    def __init__(
        self,
        metadata_type_class: Type[MetadataType],
    ):
        self.metadata_type_class = metadata_type_class
        super().__init__(attribute_name="key", description="The key of the metadata type")
