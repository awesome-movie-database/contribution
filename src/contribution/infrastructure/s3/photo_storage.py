import io
import asyncio
from typing import Iterable

from types_aiobotocore_s3 import S3Client

from contribution.domain import PhotoUrl
from contribution.application import Photo


class PhotoStorage:
    def __init__(self, client: S3Client, bucket: str):
        self._client = client
        self._bucket = bucket

    async def save_many(self, photos: Iterable[Photo]) -> None:
        async with asyncio.TaskGroup() as task_group:
            for photo in photos:
                coro = self._client.upload_fileobj(
                    Fileobj=io.BytesIO(photo.obj),
                    Bucket=self._bucket,
                    Key=photo.url,
                )
                task_group.create_task(coro)

    async def delete_by_urls(self, urls: Iterable[PhotoUrl]) -> None:
        await self._client.delete_objects(
            Bucket=self._bucket,
            Delete={"Objects": [{"Key": url} for url in urls]},
        )
