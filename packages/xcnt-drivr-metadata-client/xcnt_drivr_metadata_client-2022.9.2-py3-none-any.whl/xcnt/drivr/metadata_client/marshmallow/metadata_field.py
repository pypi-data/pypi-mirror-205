import typing
from uuid import UUID

from marshmallow import Schema, fields
from marshmallow.utils import _Missing, missing
from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.marshmallow.metadata_field_schema_creator import (
    create_or_get_marshmallow_schema_instance_for,
)


class MetadataField(fields.Field):
    """Serializer for metadata entries on objects.

    Serializes and deserializes metadata values according to the type definition of a specific
    entity type and its current metadata information.
    """

    domain_uuid_receiver_type = typing.Optional[
        typing.Union[_Missing, typing.Callable[[typing.Any], typing.Optional[UUID]]]
    ]

    def __init__(
        self,
        *,
        entity_type: str,
        domain_uuid_receiver: domain_uuid_receiver_type = missing,
        session: typing.Optional[Session] = None,
        default: typing.Any = missing,
        missing: typing.Any = missing,
        data_key: str = typing.cast(str, None),
        attribute: str = typing.cast(str, None),
        validate: typing.Optional[
            typing.Union[
                typing.Callable[[typing.Any], typing.Any],
                typing.Iterable[typing.Callable[[typing.Any], typing.Any]],
            ]
        ] = None,
        required: bool = False,
        allow_none: bool = typing.cast(bool, None),
        load_only: bool = False,
        dump_only: bool = False,
        error_messages: typing.Dict[str, str] = typing.cast(typing.Dict[str, str], None),
        **metadata: typing.Any,
    ):
        super().__init__(
            default=default,
            missing=missing,
            data_key=data_key,
            attribute=attribute,
            validate=validate,  # type: ignore
            required=required,
            allow_none=allow_none,
            load_only=load_only,
            dump_only=dump_only,
            error_messages=error_messages,
            **metadata,
        )
        self.session = session
        self.entity_type = entity_type
        self.domain_uuid_receiver = domain_uuid_receiver

    def _ensure_session(self, session: typing.Optional[typing.Any]) -> Session:
        if not hasattr(session, "commit"):
            session = self.session
        if hasattr(session, "commit"):
            return session
        else:
            raise ValueError("Could not receive session for metadata field")

    def _ensure_domain_uuid(
        self, domain_uuid: typing.Optional[typing.Union[str, UUID]] = None, obj: typing.Optional[typing.Any] = None
    ) -> typing.Optional[UUID]:
        if domain_uuid is missing and (self.domain_uuid_receiver is missing or obj is None):
            raise ValueError("No domain reference available for metadata field")

        if isinstance(domain_uuid, str):
            try:
                domain_uuid = UUID(domain_uuid)
            except ValueError:
                domain_uuid = None

        if obj is not None:
            if self.domain_uuid_receiver is not None and self.domain_uuid_receiver is not missing:
                domain_uuid = self.domain_uuid_receiver(obj)  # type: ignore

        return domain_uuid

    def _schema_for(self, session: Session, domain_uuid: UUID) -> Schema:
        return create_or_get_marshmallow_schema_instance_for(
            session=session,
            domain_uuid=domain_uuid,
            entity_type=self.entity_type,
        )

    def _serialize(
        self, value: typing.Any, attr: str, obj: typing.Any, **kwargs: typing.Any
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        if value is None:
            return None

        context = getattr(self.root, "context", None) or {}
        try:
            domain_uuid = context["domain_uuid"]
        except KeyError:
            domain_uuid = missing
        domain_uuid = self._ensure_domain_uuid(domain_uuid, obj)

        session = context.get("session", self.session)
        session = self._ensure_session(session)
        schema = self._schema_for(session, domain_uuid)

        return schema.dump(value)

    def _deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str],
        data: typing.Optional[typing.Mapping[str, typing.Any]],
        **kwargs: typing.Any,
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        if value is None:
            return None

        context = getattr(self.root, "context", None) or {}
        try:
            domain_uuid = context["domain_uuid"]
        except KeyError:
            domain_uuid = missing
        domain_uuid = self._ensure_domain_uuid(domain_uuid)

        session = context.get("session", self.session)
        session = self._ensure_session(session)
        schema = self._schema_for(session, domain_uuid)

        return schema.load(value)
