import uuid

from xcnt.drivr.metadata_client import MetadataType
from xcnt.drivr.metadata_client.lookup import MetadataLookup


class TestMetadataLookup:
    @staticmethod
    def test_metadata_lookup_for_existing_entity(session, user, special_metadata_type, really_special_metadata_type):
        user.meta.special = "special!"
        user.meta.really_special = "really_special!"
        session.commit()

        lookup = MetadataLookup(session, entity_uuid=user.uuid, domain_uuid=user.domain_uuid, entity_type="User")
        assert isinstance(lookup.types["special"], MetadataType)
        assert isinstance(lookup.types["really_special"], MetadataType)
        assert lookup.values == {"really_special": "really_special!", "special": "special!"}

    @staticmethod
    def test_metadata_lookup_for_non_existing_entity_returns_empty_results(user, session, factories):
        lookup = MetadataLookup(session, entity_uuid=user.uuid, domain_uuid=uuid.uuid4(), entity_type="User")
        assert len(lookup.types) == 0
        assert len(lookup.values) == 0

        lookup = MetadataLookup(session, entity_uuid=uuid.uuid4(), domain_uuid=user.domain_uuid, entity_type="User")
        assert len(lookup.types) == 0
        assert len(lookup.values) == 0
