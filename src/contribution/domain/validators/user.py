import re

from contribution.domain.exceptions import (
    InvalidUserNameError,
    InvalidEmailError,
    InvalidTelegramError,
)


USER_NAME_MIN_LENGTH = 5
USER_NAME_MAX_LENGTH = 64

EMAIL_VALIDATION_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
)

TELEGRAM_MIN_LENGTH = 5
TELEGRAM_MAX_LENGTH = 32


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


class ValidateEmail:
    def __call__(self, email: str) -> None:
        match = re.fullmatch(EMAIL_VALIDATION_PATTERN, email)
        if not match:
            raise InvalidEmailError()


class ValidateTelegram:
    def __call__(self, telegram: str) -> None:
        telegram_length = len(telegram)
        if (
            telegram_length < TELEGRAM_MIN_LENGTH
            or telegram_length > TELEGRAM_MAX_LENGTH
        ):
            raise InvalidTelegramError()

        for character in telegram:
            if not character.isalnum() and character != "_":
                raise InvalidTelegramError()
