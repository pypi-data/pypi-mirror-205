import contextlib
import time
from typing import Callable, ContextManager, Optional

from xcnt.cqrs.event import Registry
from xcnt.cqrs.kafka_http_client import Configuration, HTTPConsumerFetchClient

from xcnt.drivr.metadata_client.registry import metadata_registry


class Runner:
    def __init__(
        self, configuration: Configuration, registry: Registry, context: Optional[Callable[[], ContextManager]] = None
    ):
        self._configuration = configuration
        self.context = context or contextlib.suppress
        self.running = False
        self.registry = registry
        self.fetch_client = self._create_fetch_client()

    def start(self) -> None:
        with self.context():
            self.running = True
            while self.running:
                self.fetch_client.fetch_and_execute()
                time.sleep(0)

    def _create_fetch_client(self) -> HTTPConsumerFetchClient:
        client = HTTPConsumerFetchClient(self._configuration, self.registry)
        client.populate_from_registry()
        return client

    def stop(self) -> None:
        self.running = False


def init_runner_from_config(
    configuration: Configuration, context: Optional[Callable[[], ContextManager]] = None
) -> Runner:
    return Runner(configuration, metadata_registry, context)


def init_runner(consumer_group_id: str, context: Optional[Callable[[], ContextManager]] = None) -> Runner:
    configuration = Configuration.from_environment()
    configuration.group_id = consumer_group_id
    configuration.validate()
    return init_runner_from_config(configuration, context)
