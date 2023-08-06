import typing

from webargs import fields


class ListOrOne(fields.List):
    def _serialize(
        self, value: typing.Any, attr: str, obj: typing.Any, **kwargs: typing.Any
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], typing.Any]]:
        if isinstance(value, list):
            return super()._serialize(value, attr, obj, **kwargs)

        return self.inner._serialize(value, attr, obj, **kwargs)

    def _deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str],
        data: typing.Optional[typing.Mapping[str, typing.Any]],
        **kwargs: typing.Any,
    ) -> typing.Union[typing.List[typing.Any], typing.Any]:
        if isinstance(value, list):
            return super()._deserialize(value, attr, data, **kwargs)

        return self.inner._deserialize(value, attr, data, **kwargs)
