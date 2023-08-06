from typing import Any, Callable, Type

from marshmallow import Schema, pre_dump

from xcnt.drivr.metadata_client.marshmallow.metadata_field import MetadataField
from xcnt.drivr.metadata_client.marshmallow.metadata_key_value_store_field import MetadataKeyValueStoreField


class MetadataKeyValueStore(object):
    """Add MetadataKeyValueStore to Schema.

    The MetadataKeyValueStore decorator adds a MetadataKeyValueStoreField to the decorated schema.
    """

    def __init__(
        self,
        is_loader: bool = False,
        metadata_key_value_store_field_name: str = "metadata_key_value_store",
        metadata_key_value_store_field_attr: str = "metadata_key_value_store",
    ):
        self.is_loader = is_loader
        self.metadata_key_value_store_field_name = metadata_key_value_store_field_name
        self.metadata_key_value_store_field_attr = metadata_key_value_store_field_attr

    def __call__(self, cls: Type[Schema]) -> Type[Schema]:
        new_attrs = {}
        for k, v in cls._declared_fields.items():
            if isinstance(v, MetadataField):
                metadata_attribute = getattr(v, "attribute", None)
                if metadata_attribute is None:
                    metadata_attribute = k
                metadata_data_key = getattr(v, "data_key", None)
                if metadata_data_key is None:
                    metadata_data_key = metadata_attribute

                new_attrs["metadata_attr"] = metadata_attribute
                new_attrs["metadata_field"] = metadata_data_key
                new_attrs["metadata_key_value_store_field_name"] = self.metadata_key_value_store_field_name
                new_attrs["metadata_key_value_store_field_attr"] = self.metadata_key_value_store_field_attr

                new_attrs["metadata_key_value_store"] = MetadataKeyValueStoreField(
                    entity_type=v.entity_type,
                    session=v.session,
                    domain_uuid_receiver=v.domain_uuid_receiver,
                    data_key=self.metadata_key_value_store_field_attr,
                    attribute=self.metadata_key_value_store_field_name,
                    is_loader=self.is_loader,
                )
                break

        # add pre_dump
        def fill_kv_store(self: Any, obj: Any, many: bool) -> Any:
            kv_store = []
            original_metadata = getattr(obj, self.metadata_attr, None)
            if original_metadata is None:
                return obj

            for key, value in original_metadata._to_dict().items():
                kv_pair = {
                    "key": key,
                    "value": value,
                    "metadata_type_uuid": original_metadata._metadata_type_dict[key].uuid,
                    "data_type": str(original_metadata._metadata_type_dict[key].data_type).upper(),
                }
                kv_store.append(kv_pair)
            setattr(obj, self.metadata_key_value_store_field_name, kv_store)
            return obj

        cls.fill_kv_store = pre_dump(fill_kv_store)

        # add model init
        def make_model(self: Any, model: Callable[..., Any], data: dict[str, Any]) -> Any:
            metadata_kv_store = data.get(self.metadata_key_value_store_field_name, None)
            if metadata_kv_store is not None:
                if self.metadata_attr not in data:
                    data[self.metadata_attr] = {}
                for kv_pair in metadata_kv_store:
                    if kv_pair["key"] in data[self.metadata_attr]:
                        # metadata already defined
                        continue
                    values = kv_pair["value"].values()
                    value = None
                    if len(values) > 0:
                        value = next(iter(values))
                    data[self.metadata_attr][kv_pair["key"]] = value

                del data[self.metadata_key_value_store_field_name]

            return model(**data)

        return type(cls.__name__, (cls,), {**new_attrs, **{"make_model": make_model}})
