from typing import Any, Callable, Dict, Optional, Type
from uuid import UUID

import pytest
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from xcnt.drivr.metadata_client.test.conftest import User
from xcnt.drivr.metadata_client.test.search.user import UserQuery


@pytest.fixture
def user_query(session, query_class) -> UserQuery:
    return UserQuery(query_class)


@pytest.fixture
def query_class():
    return User


@pytest.fixture
def annotate_query(
    user_query: UserQuery, domain_uuid: UUID, session: Session, query_class: Type[User]
) -> Callable[[Dict[str, Any]], Query]:
    def _annotate(query_params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Query:
        context = context or {"domain_uuid": domain_uuid, "session": session}
        query = session.query(query_class)
        return user_query.apply(query, query_params, context=context)

    return _annotate
