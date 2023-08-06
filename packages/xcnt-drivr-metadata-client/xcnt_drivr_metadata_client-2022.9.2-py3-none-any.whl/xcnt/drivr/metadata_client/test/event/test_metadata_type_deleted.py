from pytest_cases import fixture_ref, parametrize_plus

from xcnt.drivr.metadata_client.test.conftest import MetadataType
from xcnt.drivr.metadata_client.test.event.conftest import DeletedTestEvent


@parametrize_plus(
    "create_event, entity",
    [
        [fixture_ref("metadata_for_user"), "User"],
        [
            fixture_ref("metadata_for_organization"),
            "Organization",
        ],
        [fixture_ref("metadata_for_component"), "Component"],
    ],
)
def test_metadata_for_selected_entities(create_event, entity, session):
    create_event.handle()
    metadata = session.query(MetadataType).filter(MetadataType.entity_type == entity).first()
    assert metadata is not None

    DeletedTestEvent(create_event.aggregate_id).handle()
    metadata = session.query(MetadataType).filter(MetadataType.entity_type == entity).first()
    assert metadata is None


@parametrize_plus(
    "create_event, entity",
    [
        [fixture_ref("metadata_for_system"), "System"],
        [
            fixture_ref("metadata_for_component_model"),
            "ComponentModel",
        ],
    ],
)
def test_metadata_for_nonselected_entities(create_event, entity, session):
    create_event.handle()
    metadata = session.query(MetadataType).filter(MetadataType.entity_type == entity).first()
    assert metadata is None

    DeletedTestEvent(create_event.aggregate_id).handle()
    metadata = session.query(MetadataType).filter(MetadataType.entity_type == entity).first()
    assert metadata is None
