from typing import Optional

from xcnt.sqlalchemy.search import fields


class MetadataFieldBase(fields.ConcreteBase):
    _entity_type: Optional[str]

    def __init__(
        self, entity_type: Optional[str] = None, attribute_name: Optional[str] = None, description: Optional[str] = None
    ):
        self.entity_type = entity_type  # type: ignore
        super().__init__(attribute_name=attribute_name, description=description)

    @property
    def entity_type(self) -> str:
        if self._entity_type is None:
            self._entity_type = self.resource.model.__name__
        assert self._entity_type is not None
        return self._entity_type

    @entity_type.setter
    def entity_type(self, value: Optional[str]) -> None:
        self._entity_type = value


class MetadataField(MetadataFieldBase):
    ...
