from typing import Iterable

from types_aiobotocore_s3 import S3Client

from contribution.domain import PhotoUrl


class PhotoStorage:
    def __init__(self, client: S3Client, bucket: str):
        self._client = client
        self._bucket = bucket

    async def delete_by_urls(self, urls: Iterable[PhotoUrl]) -> None:
        await self._client.delete_objects(
            Bucket=self._bucket,
            Delete={"Objects": [{"Key": url} for url in urls]},
        )
