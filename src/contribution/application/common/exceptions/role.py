from typing import Collection

from contribution.domain import RoleId
from .base import ApplicationError


class RolesAlreadyExistError(ApplicationError):
    def __init__(
        self,
        ids_of_existing_roles: Collection[RoleId],
    ):
        self.ids_of_existing_roles = ids_of_existing_roles


class RolesDoNotExistError(ApplicationError):
    def __init__(
        self,
        ids_of_missing_roles: Collection[RoleId],
    ):
        self.ids_of_missing_roles = ids_of_missing_roles
