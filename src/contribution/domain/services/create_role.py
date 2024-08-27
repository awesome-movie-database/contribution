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
        validate_character: ValidateRoleCharacter,
        validate_importance: ValidateRoleImportance,
    ):
        self._validate_character = validate_character
        self._validate_importane = validate_importance

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
        self._validate_character(character)
        self._validate_importane(importance)

        return Role(
            id=id,
            movie_id=movie.id,
            person_id=person.id,
            character=character,
            importance=importance,
            is_spoiler=is_spoiler,
        )
