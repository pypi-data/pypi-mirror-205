from datetime import datetime

import pytest
from sqlalchemy.orm import aliased

from xcnt.drivr.metadata_client.test.conftest import User


class TestMetadataSearch:
    @staticmethod
    def test_user_meta_search_with_single_value(
        session, user, customer_number_metadata_type, annotate_query, factories
    ):
        user.meta.customer_number = "abcdef"
        other_user = factories.User(domain_uuid=user.domain_uuid)
        other_user.meta.customer_number = "defghi"
        session.commit()

        customers = annotate_query({"meta": {"customerNumber": {"_eq": "abcdef"}}})
        assert customers.count() == 1
        customer = customers.first()
        assert customer.uuid == user.uuid

        customers = annotate_query({"meta": {"customerNumber": {"_eq": "defghi"}}})
        assert customers.count() == 1
        customer = customers.first()
        assert customer.uuid == other_user.uuid

    @staticmethod
    def test_user_meta_search_with_multiple_values(
        session, user, customer_number_metadata_type, special_metadata_type, annotate_query, factories
    ):
        user.meta.customer_number = "customer_a"
        user.meta.special = "special_a"
        other_user = factories.User(domain_uuid=user.domain_uuid)
        other_user.meta.customer_number = "customer_b"
        other_user.meta.special = "special_b"
        session.commit()

        customers = annotate_query({"meta": {"special": {"_eq": "special_a"}}})
        assert customers.count() == 1
        customer = customers.first()
        assert customer.uuid == user.uuid

        customers = annotate_query({"meta": {"customerNumber": {"_eq": "customer_b"}}})
        assert customers.count() == 1
        customer = customers.first()
        assert customer.uuid == other_user.uuid

    @pytest.mark.parametrize("query_class", [User, aliased(User)])
    @staticmethod
    def test_user_meta_birth_date(session, user, birth_date_metadata_type, annotate_query, factories):
        user.meta.birth_date = datetime(1994, 11, 27)
        other_user = factories.User(domain_uuid=user.domain_uuid)
        other_user.meta.birth_date = datetime(1988, 1, 20)
        session.commit()
        birth_date_users = annotate_query({"meta": {"birth_date": {"_lt": datetime(1994, 11, 27)}}})
        users = birth_date_users.all()
        assert len(users) == 1
        birth_date_user = users[0]
        assert birth_date_user.uuid == other_user.uuid
        # This fails with the current implementation of the sqlalchemy search library
        assert birth_date_users.count() == 1

    @staticmethod
    def test_user_meta_search_multiple_filters(
        session,
        user,
        customer_number_metadata_type,
        special_metadata_type,
        really_special_metadata_type,
        annotate_query,
        factories,
    ):
        user.meta.customer_number = "abcdef"
        user.meta.special = "special"
        user.meta.really_special = "really_special"
        other_user = factories.User(domain_uuid=user.domain_uuid)
        other_user.meta.customer_number = "defghi"
        session.commit()

        customers = annotate_query(
            {"meta": {"customerNumber": {"_eq": "abcdef"}, "special": {"_in": None}, "reallySpecial": {"_in": ""}}}
        )
        assert customers.count() == 1
        customer = customers.first()
        assert customer.uuid == user.uuid

    @staticmethod
    @pytest.mark.parametrize("_null_filter_input", [True, False])
    def test_user_meta_null_filter(
        session, user, birth_date_metadata_type, annotate_query, factories, _null_filter_input
    ):
        user.meta.birth_date = datetime(1994, 11, 27)
        other_user = factories.User(domain_uuid=user.domain_uuid)
        other_user.meta.birth_date = None
        session.commit()

        birth_date_users = annotate_query({"meta": {"birth_date": {"_null": _null_filter_input}}})
        users = birth_date_users.all()
        assert len(users) == 1
        assert birth_date_users.count() == 1

    @staticmethod
    def test_user_meta_null_no_metadata_value_data(session, user, birth_date_metadata_type, annotate_query, factories):
        user.meta.birth_date = datetime(1994, 11, 27)
        factories.User(domain_uuid=user.domain_uuid)
        session.commit()

        birth_date_users = annotate_query({"meta": {"birth_date": {"_null": True}}})
        users = birth_date_users.all()
        assert len(users) == 1
        assert birth_date_users.count() == 1

    @staticmethod
    def test_user_meta_null_mixed(session, user, birth_date_metadata_type, annotate_query, factories):
        user.meta.birth_date = datetime(1994, 11, 27)
        factories.User(domain_uuid=user.domain_uuid)
        other_user = factories.User(domain_uuid=user.domain_uuid)
        other_user.meta.birth_date = None
        session.commit()

        birth_date_users = annotate_query({"meta": {"birth_date": {"_null": True}}})
        users = birth_date_users.all()
        assert len(users) == 2
        assert birth_date_users.count() == 2

    @staticmethod
    def test_metadata_key_value_search(session, user, customer_number_metadata_type, annotate_query, factories):
        user.meta.customer_number = "my-special-customer-number"
        factories.User(domain_uuid=user.domain_uuid)
        other_user = factories.User(domain_uuid=user.domain_uuid)
        other_user.meta.customer_number = "another-customer-number"
        session.commit()

        customers_query = annotate_query(
            {
                "metadata_key_value_store": {
                    "key": {"_eq": "customer_number"},
                    "value": {"string": {"_eq": "my-special-customer-number"}},
                }
            }
        )
        users = customers_query.all()
        assert len(users) == 1
        assert users[0] == user

    @staticmethod
    def test_metadata_key_value_search_with_like(
        session, user, customer_number_metadata_type, annotate_query, factories
    ):
        user.meta.customer_number = "my-special-customer-number"
        additional_user = factories.User(domain_uuid=user.domain_uuid)
        additional_user.meta.customer_number = "my-special-phone-number"
        other_user = factories.User(domain_uuid=user.domain_uuid)
        other_user.meta.customer_number = "another-customer-number"
        session.commit()

        customers_query = annotate_query(
            {
                "metadata_key_value_store": {
                    "key": {"_eq": "customer_number"},
                    "value": {"string": {"_like": "my-special%number"}},
                }
            }
        )
        users = customers_query.all()
        assert len(users) == 2
        assert user in users
        assert additional_user in users
