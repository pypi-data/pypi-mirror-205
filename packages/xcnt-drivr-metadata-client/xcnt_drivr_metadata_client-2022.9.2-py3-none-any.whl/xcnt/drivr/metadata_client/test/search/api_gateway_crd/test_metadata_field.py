from xcnt.sqlalchemy.search.api_gateway_crd import ApiGatewayCRD

from xcnt.drivr.metadata_client.test.search.user import UserQuery


def test_plugin_usage() -> None:
    result = ApiGatewayCRD([UserQuery]).build()
    user_query = result.get_argument_collection("user-query")
    assert "meta" not in user_query.spec["spec"]["arguments"]


def test_plugin_serialization_of_key_value_store_field() -> None:
    result = ApiGatewayCRD([UserQuery]).build()
    user_query = result.get_argument_collection("user-query")
    user_arguments = user_query.spec["spec"]["arguments"]
    assert "metadata_key_value_store" in user_arguments
    key_value_store_reference = user_arguments["metadata_key_value_store"]
    key_value_store_query = result.get_argument_collection(key_value_store_reference["type"]["argumentCollectionRef"])
    key_value_store_arguments = key_value_store_query.spec["spec"]["arguments"]
    for expected_argument in ["key", "value"]:
        assert expected_argument in key_value_store_arguments

    assert "type" in key_value_store_arguments["key"]
    assert key_value_store_arguments["key"]["type"]["argumentCollectionRef"] == "string-query-field"
    assert "type" in key_value_store_arguments["value"]
    assert key_value_store_arguments["value"]["type"]["argumentCollectionRef"] == "metadata-generic-value-query-field"

    value_field = result.get_argument_collection(key_value_store_arguments["value"]["type"]["argumentCollectionRef"])
    assert value_field is not None
    for attribute in ["string", "uuid"]:
        assert attribute in value_field.spec["spec"]["arguments"]
