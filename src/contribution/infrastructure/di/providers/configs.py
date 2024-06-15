from dishka import Provider, Scope

from contribution.infrastructure.database import mongodb_config_from_env
from contribution.infrastructure.message_broker import rabbitmq_config_from_env
from contribution.infrastructure.s3 import minio_config_from_env


def configs_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(mongodb_config_from_env)
    provider.provide(rabbitmq_config_from_env)
    provider.provide(minio_config_from_env)

    return provider
