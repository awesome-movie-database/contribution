from typing import Iterable, Protocol

from contribution.application.common.value_objects import Photo


class ObjectStorage(Protocol):
    async def save_photos(self, photos: Iterable[Photo]) -> None:
        raise NotImplementedError
