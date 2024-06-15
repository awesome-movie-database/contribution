from typing import Iterable, Protocol

from contribution.domain import PhotoUrl
from contribution.application.common.value_objects import Photo


class PhotoGateway(Protocol):
    async def save_many(self, photos: Iterable[Photo]) -> None:
        raise NotImplementedError

    async def delete_by_urls(self, urls: Iterable[PhotoUrl]) -> None:
        raise NotImplementedError
