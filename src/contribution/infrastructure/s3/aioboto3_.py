from aioboto3 import Session
from aiobotocore.config import AioConfig
from types_aiobotocore_s3 import S3Client

from .config import MinIOConfig


def aioboto3_s3_client_factory(
    minio_config: MinIOConfig,
) -> S3Client:
    aioboto3_session = Session()
    client = aioboto3_session.client(
        service_name="s3",
        endpoint_url=minio_config.url,
        aws_access_key_id=minio_config.access_key,
        aws_secret_access_key=minio_config.secret_key,
        config=AioConfig(signature_version="s3v4"),
    )
    return client
