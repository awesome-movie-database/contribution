from dishka import Provider, Scope

from contribution.infrastructure.operation_id import (
    default_operation_id_factory,
    web_api_operation_id_factory,
)


def cli_operation_id_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(default_operation_id_factory)

    return provider


def web_api_operation_id_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(web_api_operation_id_factory)

    return provider
