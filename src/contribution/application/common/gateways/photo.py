from typing import Iterable, Protocol

from contribution.domain import PhotoUrl


class PhotoGateway(Protocol):
    async def delete_by_urls(self, urls: Iterable[PhotoUrl]) -> None:
        raise NotImplementedError
