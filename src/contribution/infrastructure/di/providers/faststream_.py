from dishka import Provider, Scope
from faststream.broker.message import StreamMessage


def faststream_provider_factory() -> Provider:
    provider = Provider()

    provider.from_context(provides=StreamMessage, scope=Scope.REQUEST)

    return provider
