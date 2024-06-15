from dishka import Provider, Scope
from aioboto3 import Session
from aiobotocore.config import AioConfig
from types_aiobotocore_s3 import S3Client

from contribution.infrastructure.s3 import MinIOConfig


def aioboto3_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(Session)
    provider.provide(aioboto3_s3_client_factory)

    return provider


def aioboto3_s3_client_factory(
    aioboto3_session: Session,
    minio_config: MinIOConfig,
) -> S3Client:
    client = aioboto3_session.client(
        service_name="s3",
        endpoint_url=minio_config.url,
        aws_access_key_id=minio_config.access_key,
        aws_secret_access_key=minio_config.secret_key,
        config=AioConfig(signature_version="s3v4"),
    )
    return client
