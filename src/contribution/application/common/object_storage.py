from typing import Iterable, Protocol

from contribution.domain import PhotoUrl
from contribution.application.common.value_objects import Photo


class ObjectStorage(Protocol):
    async def save_photos(self, photos: Iterable[Photo]) -> None:
        raise NotImplementedError

    async def delete_photos_by_urls(
        self,
        urls: Iterable[PhotoUrl],
    ) -> None:
        raise NotImplementedError
