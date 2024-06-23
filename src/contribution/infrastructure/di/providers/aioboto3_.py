from dishka import Provider, Scope

from contribution.infrastructure.s3 import aioboto3_s3_client_factory


def aioboto3_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(aioboto3_s3_client_factory)

    return provider
