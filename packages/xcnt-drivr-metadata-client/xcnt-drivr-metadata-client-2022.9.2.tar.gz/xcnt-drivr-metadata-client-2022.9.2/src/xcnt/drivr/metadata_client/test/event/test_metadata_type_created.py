from pytest_cases import fixture_ref, parametrize_plus

from xcnt.drivr.metadata_client.test.conftest import MetadataType


@parametrize_plus(
    "event,entity",
    [
        [fixture_ref("metadata_for_user"), "User"],
        [fixture_ref("metadata_for_organization"), "Organization"],
        [fixture_ref("metadata_for_component"), "Component"],
    ],
)
def test_metadata_created_for_selected_entities(event, entity, session):
    event.handle()
    metadata = session.query(MetadataType).filter(MetadataType.entity_type == entity).first()
    assert metadata is not None


@parametrize_plus(
    "event,entity",
    [[fixture_ref("metadata_for_system"), "System"], [fixture_ref("metadata_for_component_model"), "ComponentModel"]],
)
def test_metadata_not_created_for_nonselected_entities(event, entity, session):
    event.handle()
    metadata = session.query(MetadataType).filter(MetadataType.entity_type == entity).first()
    assert metadata is None
