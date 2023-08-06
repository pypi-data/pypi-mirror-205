from webargs import fields

from xcnt.drivr.metadata_client.model import MetadataType
from xcnt.drivr.metadata_client.view.field import ListOrOne
from xcnt.drivr.metadata_client.view.web_args_builder import WebArgsBuilder


class ListWebArgsBuilder(WebArgsBuilder):
    def field_for(self, metadata_field: MetadataType) -> fields.Field:
        return ListOrOne(super().field_for(metadata_field), required=False)
