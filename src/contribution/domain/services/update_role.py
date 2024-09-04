from contribution.domain.validators import (
    ValidateRoleCharacter,
    ValidateRoleImportance,
)
from contribution.domain.models import Role
from contribution.domain.maybe import Maybe


class UpdateRole:
    def __init__(
        self,
        validate_character: ValidateRoleCharacter,
        validate_importance: ValidateRoleImportance,
    ):
        self._validate_character = validate_character
        self._validate_importane = validate_importance

    def __call__(
        self,
        role: Role,
        *,
        character: Maybe[str],
        importance: Maybe[int],
        is_spoiler: Maybe[bool],
    ) -> None:
        if character.is_set:
            self._validate_character(character.value)
            role.character = character.value
        if importance.is_set:
            self._validate_importane(importance.value)
            role.importance = importance.value
        if is_spoiler.is_set:
            role.is_spoiler = is_spoiler.value
