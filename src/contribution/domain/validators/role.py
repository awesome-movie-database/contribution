from contribution.domain.exceptions import (
    InvalidRoleCharacterError,
    InvalidRoleImportanceError,
)


ROLE_CHARACTER_MIN_LENGTH = 1
ROLE_CHARACTER_MAX_LENGTH = 64

MIN_ROLE_IMPORTANCE = 1


class ValidateRoleCharacter:
    def __call__(self, character: str) -> None:
        character_length = len(character)

        if (
            character_length < ROLE_CHARACTER_MIN_LENGTH
            or character_length > ROLE_CHARACTER_MAX_LENGTH
        ):
            raise InvalidRoleCharacterError()


class ValidateRoleImportance:
    def __call__(self, importance: int) -> None:
        if importance < MIN_ROLE_IMPORTANCE:
            raise InvalidRoleImportanceError()
