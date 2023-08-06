import typing
from weakref import ref

from sqlalchemy import and_
from sqlalchemy.sql.expression import ClauseElement, select
from webargs import fields

from xcnt.drivr.metadata_client.model import (
    INITIATED_METADATA_VALUE_CLASSES,
    INITIATED_METADATA_VALUE_LOOKUP_CLASSES,
    MetadataType,
    MetadataValue,
    MetadataValueLookup,
)


class MetadataSQLAlchemyField(fields.Field):
    def __init__(self, field: fields.Field, metadata_type: MetadataType, **kwargs: typing.Any):
        self.inner = field
        self.metadata_type = metadata_type
        super().__init__(**kwargs)

    @property
    def value_model_class(self) -> typing.Type[MetadataValue]:
        return INITIATED_METADATA_VALUE_CLASSES[self.metadata_type.entity_type]

    @property
    def value_lookup_model_class(self) -> typing.Type[MetadataValueLookup]:
        return INITIATED_METADATA_VALUE_LOOKUP_CLASSES[self.metadata_type.entity_type]

    @property  # type: ignore
    def parent(self) -> typing.Any:  # type: ignore
        parent = getattr(self, "_parent", lambda: None)
        return parent()

    @parent.setter  # type: ignore
    def parent(self, value: typing.Any) -> None:
        self._parent = ref(value)

    def _serialize(self, value: typing.Any, attr: str, obj: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.inner._serialize(value, attr, obj, **kwargs)

    def _deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str],
        data: typing.Optional[typing.Mapping[str, typing.Any]],
        **kwargs: typing.Any,
    ) -> typing.Any:
        deserialized = self.inner._deserialize(value, attr, data, **kwargs)
        metadata_type_clause = self.value_lookup_model_class.metadata_type_uuid == self.metadata_type.uuid
        column = self.value_model_class.value_column_for(self.metadata_type.data_type)

        clause: ClauseElement
        if isinstance(deserialized, list):
            clause = column.in_(deserialized)
        else:
            clause = column == deserialized

        return (
            select([self.value_lookup_model_class.entity_uuid])
            .join(
                self.value_model_class,
                self.value_lookup_model_class.metadata_value_uuid == self.value_model_class.uuid,
                isouter=True,
            )
            .where(and_(metadata_type_clause, clause))
        )
