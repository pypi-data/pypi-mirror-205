from __future__ import annotations

from enum import Enum
from typing import Union

from xcnt.cqrs.event.generator import Generator


class DataTypeEnum(Enum):
    """The `metadata-data-type` enum lists the various data types that can be associated with `MetadataType` entities.

    Each `MetadataType` entity defines a specific type of metadata that can be
    added to a specific DRIVR entity, such as _User_, _System_, or _Service_.
    """

    __graphql_name__ = "MetadataDataType"

    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
    UUID = "UUID"

    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################

    # IMAGE = "image"
    # DOCUMENT = "document"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, item: Union[str, DataTypeEnum]) -> DataTypeEnum:
        if isinstance(item, DataTypeEnum):
            return item

        for data_type in cls:
            if data_type.value.upper() == item.upper():
                return data_type
        raise KeyError(f"Did not find data type {item}")


DataTypeEnum.BOOLEAN.__doc__ = "A boolean data type represents a true or false value."
DataTypeEnum.FLOAT.__doc__ = "A float data type represents a decimal number"
DataTypeEnum.INTEGER.__doc__ = "An integer data type represents a whole number."
DataTypeEnum.STRING.__doc__ = "A string data type represents a sequence of characters."
DataTypeEnum.TIMESTAMP.__doc__ = "A timestamp data type represents a point in time."
DataTypeEnum.UUID.__doc__ = "A UUID data type represents a universally unique identifier."

Generator.add_converter(DataTypeEnum, DataTypeEnum.from_string)


class MetadataValueFeatureEnum(Enum):
    # Disables all default value indexes.
    DISABLE_VALUE_INDEXES = "disable_value_indexes"
    # Ensures a string index to be generated with an SHA hash instead of the normal ones.
    ENABLE_STRING_INDEX_BY_SHA_HASH = "enable_string_index_by_sha_hash"
    # Add an index for the metadata type uuid reference.
    ENABLE_METADATA_TYPE_INDEX = "enable_metadata_type_index"
    # Add a gin index on statements supporting like, currently string and uuid.
    ENABLE_GIN_INDEX_FOR_LIKE = "enable_gin_index_for_like"
