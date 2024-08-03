from typing import Collection

from contribution.domain import RoleId
from .base import ApplicationError


class RolesAlreadyExistError(ApplicationError):
    def __init__(self, role_ids: Collection[RoleId]):
        self.role_ids = role_ids


class RolesDoNotExistError(ApplicationError):
    def __init__(self, role_ids: Collection[RoleId]):
        self.role_ids = role_ids
