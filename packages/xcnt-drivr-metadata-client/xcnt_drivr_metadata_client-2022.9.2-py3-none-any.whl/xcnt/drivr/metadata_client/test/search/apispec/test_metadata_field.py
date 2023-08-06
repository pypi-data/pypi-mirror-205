from typing import Any, Callable, Dict

import pytest
from apispec import APISpec
from apispec.utils import build_reference
from xcnt.sqlalchemy.search.apispec import SearchParamPlugin

from xcnt.drivr.metadata_client.search.metadata_key_value_store_field import (
    MetadataGenericValueField,
    MetadataKeyValueStoreField,
)
from xcnt.drivr.metadata_client.test.search.user import UserQuery


@pytest.fixture
def api_spec() -> APISpec:
    return APISpec(title="Test", version="1.0.0", openapi_version="3.0.0", plugins=(SearchParamPlugin(),))


@pytest.fixture
def get_parameters(api_spec: APISpec) -> Callable[[], Dict[str, Any]]:
    def _get_parameters() -> Dict[str, Any]:
        return api_spec.to_dict()["components"]["parameters"]

    return _get_parameters


def test_plugin_usage(api_spec: APISpec, get_parameters) -> None:
    parameter = {"content": {"application/json": {"schema": UserQuery.__name__}}}
    api_spec.components.parameter("where", "query", parameter)
    params = get_parameters()
    schema_reference = params["where"]["content"]["application/json"]["schema"]
    assert schema_reference == build_reference("schema", api_spec.openapi_version.major, UserQuery.__name__)

    schema = api_spec.components.schemas[UserQuery.__name__]
    assert schema["properties"]["meta"]["additionalProperties"]["type"] == "object"


def test_plugin_usage_for_metadata_key_value_storage_field(api_spec: APISpec, get_parameters):
    parameter = {"content": {"application/json": {"schema": UserQuery.__name__}}}
    api_spec.components.parameter("where", "query", parameter)
    get_parameters()
    schema = api_spec.components.schemas[UserQuery.__name__]
    assert schema["properties"]["metadata_key_value_store"] == build_reference(
        "schema", api_spec.openapi_version.major, MetadataKeyValueStoreField.__name__
    )

    schema = api_spec.components.schemas[MetadataKeyValueStoreField.__name__]
    for expected_attribute in ["key", "value"]:
        assert expected_attribute in schema["properties"]

    assert schema["properties"]["value"] == build_reference(
        "schema", api_spec.openapi_version.major, MetadataGenericValueField.__name__
    )

    schema = api_spec.components.schemas[MetadataGenericValueField.__name__]
    for expected_property in ["float", "uuid", "integer"]:
        assert expected_property in schema["properties"]
