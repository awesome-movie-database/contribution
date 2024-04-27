from typing import Sequence

from contribution.domain.value_objects import RoleId
from .base import ApplicationError


class RolesDoNotExistError(ApplicationError):
    def __init__(
        self,
        ids_of_missing_roles: Sequence[RoleId],
    ):
        self.ids_of_missing_roles = ids_of_missing_roles
