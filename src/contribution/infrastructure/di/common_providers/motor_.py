from dishka import Provider, Scope

from contribution.infrastructure.database import (
    motor_client_factory,
    motor_session_factory,
    motor_database_factory,
)


def motor_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(motor_client_factory, scope=Scope.APP)
    provider.provide(motor_session_factory)
    provider.provide(motor_database_factory)

    return provider
