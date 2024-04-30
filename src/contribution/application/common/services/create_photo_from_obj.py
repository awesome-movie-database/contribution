from uuid import uuid4

from contribution.domain.value_objects import PhotoUrl
from contribution.application.common.value_objects import Photo


class CreatePhotoFromObj:
    def __call__(self, obj: bytes) -> Photo:
        photo_url = PhotoUrl(uuid4().hex)
        return Photo(obj, photo_url)