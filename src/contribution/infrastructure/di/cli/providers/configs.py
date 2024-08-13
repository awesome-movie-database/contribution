from dishka import Provider, Scope

from contribution.infrastructure.database import mongodb_config_from_env


def cli_configs_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(mongodb_config_from_env)

    return provider
