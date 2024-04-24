from contribution.domain.value_objects import RoleId
from contribution.domain.validators import (
    ValidateRoleCharacter,
    ValidateRoleImportance,
)
from contribution.domain.entities import (
    Role,
    Movie,
    Person,
)


class CreateRole:
    def __init__(
        self,
        validate_role_character: ValidateRoleCharacter,
        validate_role_importance: ValidateRoleImportance,
    ):
        self._validate_role_character = validate_role_character
        self._validate_role_importane = validate_role_importance

    def __call__(
        self,
        *,
        id: RoleId,
        movie: Movie,
        person: Person,
        character: str,
        importance: int,
        is_spoiler: bool,
    ) -> Role:
        self._validate_role_character(character)
        self._validate_role_importane(importance)

        return Role(
            id=id,
            movie_id=movie.id,
            person_id=person.id,
            character=character,
            importance=importance,
            is_spoiler=is_spoiler,
        )
