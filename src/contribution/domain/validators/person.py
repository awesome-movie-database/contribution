from contribution.domain.exceptions import (
    InvalidPersonFirstNameError,
    InvalidPersonLastNameError,
)


PERSON_FIRST_NAME_MIN_LENGTH = 1
PERSON_FIRST_NAME_MAX_LENGTH = 128

PERSON_LAST_NAME_MIN_LENGTH = 1
PERSON_LAST_NAME_MAX_LENGTH = 128


class ValidatePersonFirstName:
    def __call__(self, first_name: str) -> None:
        first_name_length = len(first_name)

        if (
            first_name_length < PERSON_FIRST_NAME_MIN_LENGTH
            or first_name_length > PERSON_FIRST_NAME_MAX_LENGTH
        ):
            raise InvalidPersonFirstNameError()


class ValidatePersonLastName:
    def __call__(self, last_name: str) -> None:
        last_name_length = len(last_name)

        if (
            last_name_length < PERSON_LAST_NAME_MIN_LENGTH
            or last_name_length > PERSON_FIRST_NAME_MAX_LENGTH
        ):
            raise InvalidPersonLastNameError()
