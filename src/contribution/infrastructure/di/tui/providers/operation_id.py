from dishka import Provider, Scope

from contribution.infrastructure.operation_id.default import (
    default_operation_id_factory,
)


def tui_operation_id_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(default_operation_id_factory)

    return provider
