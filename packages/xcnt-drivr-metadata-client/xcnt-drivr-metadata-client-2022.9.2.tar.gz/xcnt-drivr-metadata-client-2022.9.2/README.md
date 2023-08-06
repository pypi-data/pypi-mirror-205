# drivr-metadata-client

This library adds support to PostgreSQL-`SQLAlchemy` backed `cqrs` Microservices, to enable setting custom metadata configurations on a domain level for specific entities.

For this, it requires information on the Metadata configuration by listening to events from the [Metadata service](https://github.com/xcnt/drivr-metadata).
It provides methods to configure `marshmallow` Schemas with a metadata field which helps to serialize and deserialize the currently valid metadata configuration.

The `Entity Types` recognized by the `Metadata client library` and the `Data Types` supported can be found [here](https://github.com/xcnt/drivr-metadata/blob/develop/doc/spec.md).

## Quick Start

1. Enable the drivr metadata configuration by adding for specific entity types the value models:

```python

from uuid import UUID

from sqlalchemy import Column, text

from xcnt.cqrs.event import registry

from xcnt.drivr.metadata_client import (
    metadata_type_model_for,
    metadata_value_model_for,
    register_metadata_events_for,
    MetadataField,

)
from xcnt.drivr.metadata_client.enum import MetadataValueFeatureEnum

from xcnt.drivr.my_custom_service import db


class User(db.Model):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    domain_uuid = Column(UUID(as_uuid=True), nullable=True)
    meta = MetadataField(entity_type="User", domain_uuid=domain_uuid)  # ensure entity_type is always in `PascalCase`

MetadataType = metadata_type_model_for(db.Model, db.session)

features = [MetadataValueFeatureEnum.DISABLE_VALUE_INDEXES, MetadataValueFeatureEnum.ENABLE_METADATA_TYPE_INDEX]  # This is optional to disable indexes for metadata values.

UserMetadataValue = metadata_value_model_for(db.Model, EntityTypeEnum.USER, User, features)
register_metadata_events_for(
    registry, UserMetadataValue, EntityTypeEnum.USER, db.session
)

```

2. Generate necessary alembic migrations

In Bash:

```bash
alembic revision -m "add metadata values" --autogenerate
```

3. Consume metadata type events to get the configuration from the [Metadata service](https://github.com/xcnt/drivr-metadata):

```python
from xcnt.drivr.metadata_client import init_runner

runner = init_runner(
  context=app.app_context, # pass the client service context to poll for new Metadata events pushed to kafka
  consumer_group_id='fill this with a unique id for a consumer group',
)
runner.start()
```

Alternatively, you can also add an already prepared configuration object.

```python
from xcnt.drivr.metadata_client import init_runner_from_config

runner = init_runner_from_config(
  configuration=my_pre_made_configuration,
  context=app.app_context, # pass the client service context to poll for new Metadata events pushed to kafka
)
runner.start()
```

4. Use Metadata value command to support setting metadata values

```python
from uuid import UUID

from xcnt.cqrs.command import Attribute
from xcnt.drivr.metadata_client import MetadataValueCommand
from xcnt.drivr.metadata_client import EntityTypeEnum

from xcnt.drivr.my_custom_service import db
from xcnt.drivr.my_custom_service.model import User
from xcnt.drivr.my_custom_service.command.base import BaseCommand


class UserCommand(MetadataValueCommand, BaseCommand):
    sqlalchemy_model = User
    session = db.session
    metadata_entity_type = EntityTypeEnum.USER

    domain_uuid: Attribute[UUID]

    @property
    def metadata_domain_uuid(self) -> UUID:
        return self.domain_uuid

```

5. Use command to set metadata values

```python
domain_uuid = get_current_domain_uuid()
user_command = UserCommand(uuid4(), domain_uuid=domain_uuid, metadata={"birth_date": datetime(2020, 1, 30)})
user_command.execute()
```

6. Specify your marshmallow schema

```python
from marshmallow import Schema
from xcnt.drivr.metadata_client import MarshmallowMetadataField as MetadataField

class UserSchema(Schema):
    meta = MetadataField(
        entity_type=EntityTypeEnum.USER, session=db.session
    )
```

7. Use the schema to serialize a user

```python
from xcnt.drivr.my_custom_service import db
from xcnt.drivr.my_custom_service.model import User

user_uuid = get_user_uuid()

user = db.session.query(User).filter(User.uuid == user_uuid).first()
result = UserSchema(context=dict(domain_uuid=user.domain_uuid)).dump(user)
assert "metadata" in result
print(result)
```

8. Use the schema to deserialize user information

```python
from uuid import uuid4

domain_uuid = get_current_domain_uuid()

user_dict = {
    "uuid": uuid4(),
    "domain_uuid": domain_uuid,
    "metadata": {
        "birth_date": datetime(1997, 11, 27).isoformat(),
    }
}

result = UserSchema(context=dict(domain_uuid=domain_uuid)).load(user_dict)
assert result["metadata"]["birth_date"] == datetime(1997, 11, 27)
```

9. Use the metadata fields for query filtering

```python
from flask import request
from xcnt.drivr.metadata_client import filter_for
from myapp import session

def my_view():
  domain_uuid = get_current_domain_uuid()

  filter_func = filter_for(
    entity_type="User",
    domain_uuid=domain_uuid,
    metadata_field_name="metadata",  # Defaults to 'metadata'
  )

  return session.query(User).filter(filter_func(request.args)).all()

```

10. Use optionally [sqlalchemy search](https://github.com/xcnt/sqlalchemy-search/) plugin for metadata fields

```python
from xcnt.sqlalchemy.search import Resource
from xcnt.drivr.metadata_client.search import MetadataField as MetadataSearchField
from xcnt.drivr.metadata_client.search import MetadataKeyValueStoreField as MetadataKeyValueStoreSearchField


class UserQuery(Resource):
  class Meta:
    model = User

  # If you want to search with key attributes e.g.
  # {"customer_number": {"_eq": "abc"}}
  meta = MetadataSearchField()

  # If you want to search via generic key value pairs e.g.
  # {"key": {"_eq": "customer_number"}, "value": {"string": {"_eq": "abc"}}}
  metadata_key_value_store = MetadataKeyValueStoreSearchField()

```

## Basic Configurations

To use the library, the client service is expected to configure `metadata_type_model_for`, `metadata_value_model_for`, `register_metadata_events_for`. They are accessible in the `xcnt.drivr.metadata_client` package.

| Configuration                  | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Returns                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `metadata_type_model_for`      | This configuration method requires a `declarative_base` as well as a `session` object to create `MetadataType` table in the local database where all received metadata values are stored                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Initialized `MetadataType` model class                               |
| `metadata_value_model_for`     | The configuration method requires a `declarative_base`, `entity_type` as well as a `reference_entity_model` to create `{EntityType}MetadataValue` table specific to the enity type in the local database where all received metadata values for the passed entity type are stored. You can `disable indexes on values` on these tables by adding `MetadataValueFeatureEnum.DISABLE_VALUE_INDEXES` into the `features` configuration. `MetadataValueFeatureEnum.ENABLE_METADATA_TYPE_INDEX` lets you configure if an index should be added to the metadata type foreign key. `ENABLE_GIN_INDEX_FOR_LIKE` allows to generate an optimized index for LIKE queries against strings and uuids. | Initialized `MetadataValue` class specific to the passed entity type |
| `register_metadata_events_for` | The configuration method requires a `Registry` object, initialized `MetadataValue` model, `enity_type` as well as a `session` object to create and handle `entity_type` specific `MetadataValueEvents`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Mapping dictionary for each event type with the actual `Event`       |

## Helpful Links and Misc. Documentation

[Jamboard Metadata Lookup](https://jamboard.google.com/d/1904cigdro075Y8dxkA9PkeZX_7rrO1pzoY7TDGL7b14/viewer)
