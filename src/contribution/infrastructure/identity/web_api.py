from fastapi import Request

from contribution.domain import UserId
from .permissions_storage import PermissionsStorage
from .identity_provider import RawIdentityProvider


def web_api_identity_provider_factory(
    request: Request,
    permissions_storage: PermissionsStorage,
) -> RawIdentityProvider:
    user_id_as_str = request.headers.get("X-Current-User-Id", None)
    if user_id_as_str:
        user_id = UserId(user_id_as_str)
    else:
        user_id = None

    return RawIdentityProvider(
        user_id=user_id,
        permissions_storage=permissions_storage,
    )
