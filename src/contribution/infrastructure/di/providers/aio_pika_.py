from dishka import Provider, Scope

from contribution.infrastructure.message_broker import (
    aio_pika_connection_factory,
    aio_pika_channel_factory,
    aio_pika_exchange_factory,
)


def aio_pika_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(aio_pika_connection_factory, scope=Scope.APP)
    provider.provide(aio_pika_channel_factory)
    provider.provide(aio_pika_exchange_factory)

    return provider
