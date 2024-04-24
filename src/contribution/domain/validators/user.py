from contribution.domain.exceptions import InvalidUserNameError


USER_NAME_MIN_LENGTH = 5
USER_NAME_MAX_LENGTH = 64


class ValidateUserName:
    def __call__(self, name: str) -> None:
        name_length = len(name)
        name_has_spaces = len(name.split()) != 1

        if (
            name_length < USER_NAME_MIN_LENGTH
            or name_length > USER_NAME_MAX_LENGTH
            or name_has_spaces
        ):
            raise InvalidUserNameError
