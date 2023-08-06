from functools import cached_property
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeMeta


class MetadataBaseLookupParserMixin:
    model: DeclarativeMeta

    @property
    def parse_context(self) -> Dict[str, Any]:
        return getattr(self, "_parse_context", None) or {}

    @parse_context.setter
    def parse_context(self, context: Dict[str, Any]) -> None:
        self._parse_context = context

    @cached_property
    def model_primary_key_name(self) -> str:
        inspect_result = inspect(self.model)
        while inspect_result.is_aliased_class:
            inspect_result = inspect(inspect_result.mapper)
        return inspect_result.primary_key[0].name

    @property
    def model_primary_key(self) -> Any:
        return getattr(self.model, self.model_primary_key_name)

    @property
    def domain_uuid(self) -> Optional[UUID]:
        domain_uuid = self.parse_context.get("domain_uuid", None)
        if isinstance(domain_uuid, str):
            try:
                domain_uuid = UUID(domain_uuid)
                self.parse_context["domain_uuid"] = domain_uuid
            except ValueError:
                pass

        if isinstance(domain_uuid, UUID):
            return domain_uuid

        return None
