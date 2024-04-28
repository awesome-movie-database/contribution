from dataclasses import dataclass

from contribution.domain.value_objects import PhotoUrl


@dataclass(frozen=True, slots=True)
class Photo:
    obj: bytes
    url: PhotoUrl
