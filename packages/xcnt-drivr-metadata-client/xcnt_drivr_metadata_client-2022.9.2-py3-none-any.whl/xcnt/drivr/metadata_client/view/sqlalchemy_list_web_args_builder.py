from webargs import fields

from xcnt.drivr.metadata_client.model import MetadataType
from xcnt.drivr.metadata_client.view.field import MetadataSQLAlchemyField
from xcnt.drivr.metadata_client.view.list_web_args_builder import ListWebArgsBuilder


class SqalchemyListWebArgsBuilder(ListWebArgsBuilder):
    def field_for(self, metadata_field: MetadataType) -> fields.Field:
        return MetadataSQLAlchemyField(super().field_for(metadata_field), metadata_type=metadata_field, required=False)
