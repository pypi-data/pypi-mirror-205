from xcnt.cqrs.event import Registry

from xcnt.drivr.metadata_client import event as metadata_events

metadata_registry = Registry()

for event in metadata_events.ALL_METADATA_TYPE_EVENTS:
    # TODO: remove type ignore once mypy plugin is fixed
    # Error: Argument 1 to "register" of "Registry" has incompatible type "EventMeta"; expected "Type[<nothing>]"
    metadata_registry.register(event)  # type: ignore
