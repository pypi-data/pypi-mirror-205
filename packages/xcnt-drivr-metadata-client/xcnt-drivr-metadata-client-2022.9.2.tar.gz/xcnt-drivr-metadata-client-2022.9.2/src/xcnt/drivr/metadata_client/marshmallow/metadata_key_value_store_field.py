import typing
from uuid import UUID

from marshmallow import ValidationError, fields
from marshmallow.utils import _Missing, missing
from sqlalchemy.orm import Session

from xcnt.drivr.metadata_client.marshmallow.metadata_key_value_pair_schema_creator import (
    MetadataKeyValuePairSchema,
    create_key_value_pairs_for,
)


class MetadataKeyValueStoreField(fields.List):
    """Serializes and deserializes metadata in a list of metadata key value pairs.

    De-/Serializes values according to the type definition of a specific
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
        session: Session | None = None,
        is_loader: bool = False,
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
        error_messages: dict[str, str] = typing.cast(dict[str, str], None),
        **metadata: typing.Any,
    ):
        super().__init__(
            fields.Nested(MetadataKeyValuePairSchema),
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
        self.is_loader = is_loader

    def _ensure_session(self, session: typing.Any | None) -> Session:
        if not hasattr(session, "commit"):
            session = self.session
        if hasattr(session, "commit"):
            return session
        else:
            raise ValueError("Could not receive session for metadata field")

    def _ensure_domain_uuid(
        self, domain_uuid: typing.Union[str, UUID] | None = None, obj: typing.Any | None = None
    ) -> UUID | None:
        if domain_uuid is missing and self.domain_uuid_receiver is missing:
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

    def _key_value_pairs_for(self, session: Session, domain_uuid: UUID) -> dict[str, MetadataKeyValuePairSchema]:
        return create_key_value_pairs_for(
            session=session,
            domain_uuid=domain_uuid,
            entity_type=self.entity_type,
            loader_schema=self.is_loader,
        )

    def _serialize(self, value: typing.Any, attr: str, obj: typing.Any, **kwargs: typing.Any) -> list[str] | None:
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

        key_value_pairs = self._key_value_pairs_for(session, domain_uuid)
        result = []

        for kvpair in value:
            key = kvpair["key"]
            schema = key_value_pairs[key]
            metakvpair = schema().dump(kvpair)
            result.append(metakvpair)

        return result

    def _deserialize(
        self,
        value: typing.Any,
        attr: str | None,
        data: typing.Mapping[str, typing.Any] | None,
        **kwargs: typing.Any,
    ) -> list[typing.Any] | None:
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

        key_value_pairs = self._key_value_pairs_for(session, domain_uuid)
        result = []

        for kv_pair in value:
            assert isinstance(kv_pair, dict)
            key = kv_pair.get("key", None)
            if key is None:
                raise ValidationError("no key in key-value pair")
            schema = key_value_pairs.get(key, None)
            if schema is None:
                raise ValidationError(f"no metadata {key} defined on {self.entity_type}")
            meta_kv_pair = schema().load(kv_pair)
            result.append(meta_kv_pair)

        return result
