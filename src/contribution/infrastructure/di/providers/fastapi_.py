from fastapi import Request
from dishka import Provider, Scope


def fastapi_provider_factory() -> Provider:
    provider = Provider()

    provider.from_context(provides=Request, scope=Scope.REQUEST)

    return provider
