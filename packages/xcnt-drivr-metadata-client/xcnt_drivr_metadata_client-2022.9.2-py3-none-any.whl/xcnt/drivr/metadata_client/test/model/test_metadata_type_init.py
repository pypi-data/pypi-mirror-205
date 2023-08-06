from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import pytest

from xcnt.drivr.metadata_client.enum import DataTypeEnum
from xcnt.drivr.metadata_client.test.conftest import MetadataType


def test_metadata_entry_add(session, factories) -> None:
    metadata_type = factories.MetadataType()
    assert isinstance(metadata_type, MetadataType)


default_value_configs = [
    {"data_type": DataTypeEnum.STRING, "value": "test", "default_value_postfix": "string"},
    {"data_type": DataTypeEnum.BOOLEAN, "value": False, "default_value_postfix": "boolean"},
    {"data_type": DataTypeEnum.FLOAT, "value": 2.5, "default_value_postfix": "float"},
    {"data_type": DataTypeEnum.UUID, "value": uuid4(), "default_value_postfix": "uuid"},
    {"data_type": DataTypeEnum.INTEGER, "value": 2, "default_value_postfix": "integer"},
    {
        "data_type": DataTypeEnum.TIMESTAMP,
        "value": datetime.now().replace(tzinfo=timezone.utc),
        "default_value_postfix": "timestamp",
    },
    #########################################################################
    #                                                                       #
    #  CAUTION:                                                             #
    #  Commented out until document and image are fully supported by DRIVR  #
    #                                                                       #
    #########################################################################
    # {"data_type": DataTypeEnum.DOCUMENT, "value": uuid4(), "default_value_postfix": "uuid"},
    # {"data_type": DataTypeEnum.IMAGE, "value": uuid4(), "default_value_postfix": "uuid"},
]
default_value_config_tuples = [
    (
        default_config["data_type"],
        default_config["value"],
        default_config["default_value_postfix"],
    )
    for default_config in default_value_configs
]


@pytest.mark.parametrize("data_type,value,default_value_postfix", default_value_config_tuples)
def test_metadata_default_value_set_retrieve(
    session, data_type: DataTypeEnum, value: Any, default_value_postfix: str, factories
) -> None:
    metadata_type = factories.MetadataType(data_type=data_type)
    metadata_type.default_value = value
    assert metadata_type.default_value == value
    assert getattr(metadata_type, f"default_value_{default_value_postfix}") == value
