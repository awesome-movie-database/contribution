from typing import Protocol, Sequence

from contribution.application.common.value_objects import Photo


class ObjectStorage(Protocol):
    async def save_photo_seq(self, photos: Sequence[Photo]) -> None:
        raise NotImplementedError
