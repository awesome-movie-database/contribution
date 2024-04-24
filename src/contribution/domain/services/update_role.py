from contribution.domain.validators import (
    ValidateRoleCharacter,
    ValidateRoleImportance,
)
from contribution.domain.entities import Role
from contribution.domain.maybe import Maybe


class UpdateRole:
    def __init__(
        self,
        validate_role_character: ValidateRoleCharacter,
        validate_role_importance: ValidateRoleImportance,
    ):
        self._validate_role_character = validate_role_character
        self._validate_role_importane = validate_role_importance

    def __call__(
        self,
        role: Role,
        *,
        character: Maybe[str],
        importance: Maybe[int],
        is_spoiler: Maybe[bool],
    ) -> None:
        if character.is_set:
            self._validate_role_character(character.value)
            role.character = character.value
        if importance.is_set:
            self._validate_role_importane(importance.value)
            role.importance = importance.value
        if is_spoiler.is_set:
            role.is_spoiler = is_spoiler.value
