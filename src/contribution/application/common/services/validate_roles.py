from typing import Iterable

from contribution.domain import (
    ContributionRole,
    ValidateRoleCharacter,
    ValidateRoleImportance,
)


class ValidateRoles:
    def __init__(
        self,
        validate_role_character: ValidateRoleCharacter,
        validate_role_importance: ValidateRoleImportance,
    ):
        self._validate_role_character = validate_role_character
        self._validate_role_importance = validate_role_importance

    def __call__(self, roles: Iterable[ContributionRole]) -> None:
        for role in roles:
            self._validate_role_character(role.character)
            self._validate_role_importance(role.importance)
