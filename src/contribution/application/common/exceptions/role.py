from typing import Sequence

from contribution.domain import RoleId
from .base import ApplicationError


class RolesAlreadyExistError(ApplicationError):
    def __init__(
        self,
        ids_of_existing_roles: Sequence[RoleId],
    ):
        self.ids_of_existing_roles = ids_of_existing_roles


class RolesDoNotExistError(ApplicationError):
    def __init__(
        self,
        ids_of_missing_roles: Sequence[RoleId],
    ):
        self.ids_of_missing_roles = ids_of_missing_roles
