from dishka import Provider, Scope

from contribution.infrastructure.operation_id.event_consumer import (
    event_consumer_operation_id_factory,
)


def event_consumer_operation_id_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(event_consumer_operation_id_factory)

    return provider
