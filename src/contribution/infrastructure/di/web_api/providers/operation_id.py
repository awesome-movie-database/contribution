from dishka import Provider, Scope

from contribution.infrastructure.operation_id.web_api import (
    web_api_operation_id_factory,
)


def web_api_operation_id_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(web_api_operation_id_factory)

    return provider
