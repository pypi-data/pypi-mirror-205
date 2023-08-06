from typing import Any, Dict, Optional

from xcnt.sqlalchemy.search import EvaluationErrorCode, EvaluationResult, FieldParser, FieldPlugin, fields
from xcnt.sqlalchemy.search.parser.evaluation_result import key_derivations
from xcnt.sqlalchemy.search.parser.flow_exception import ReturnAll

from xcnt.drivr.metadata_client.model import MetadataType
from xcnt.drivr.metadata_client.search.metadata_field import MetadataField
from xcnt.drivr.metadata_client.search.metadata_item import MetadataItem
from xcnt.drivr.metadata_client.search.parser.keyed_lookup_parser_mixin import KeyedLookupParserMixin


class MetadataFieldParser(FieldPlugin[MetadataField, Dict[str, Any]], KeyedLookupParserMixin):
    @classmethod
    def supports(self, entity: fields.BaseField) -> bool:
        return isinstance(entity, MetadataField)

    @property
    def entity_type(self) -> str:
        return self.resource_field.entity_type

    @property
    def _metadata_entities(self) -> Dict[str, MetadataType]:
        return self._lookup.lookup_dict

    def parse(self, parse_context: Dict[str, Any]) -> EvaluationResult:
        self.parse_context = parse_context
        if self.domain_uuid is None or self.session is None:
            # No support for metadata queries if no domain uuid is provided or no
            # db session for getting the configured metadata fields is provided
            raise ReturnAll()

        entities = self._metadata_entities
        for key in self.query.keys():
            for check_key in key_derivations(key):
                if check_key in entities:
                    break

            if check_key not in entities:
                self.errors[key] = EvaluationErrorCode.UNKNOWN_FIELD
                continue

            evaluation_result = self._result_for(key, entities[check_key])
            if evaluation_result is not None:
                self.sub_results.append(evaluation_result)

        if len(self.sub_results) == 0:
            raise ReturnAll()

        return self._result_from_state()

    def _result_for(self, check_key: str, metadata_type: MetadataType) -> Optional[EvaluationResult]:
        try:
            field = MetadataItem(metadata_type, attribute_name=check_key)
            field.resource = self.resource_field.resource
            field_parser = FieldParser(check_key, self.query[check_key], field)
            return field_parser.parse(self.parse_context)
        except ReturnAll:
            return None
