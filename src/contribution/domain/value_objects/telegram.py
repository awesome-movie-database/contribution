from dataclasses import dataclass

from contribution.domain.exceptions import InvalidTelegramError


TELEGRAM_MIN_LENGTH = 5
TELEGRAM_MAX_LENGTH = 32


@dataclass(frozen=True, slots=True)
class Telegram:
    value: str

    def __post_init__(self) -> None:
        telegram_length = len(self.value)
        if (
            telegram_length < TELEGRAM_MIN_LENGTH
            or telegram_length > TELEGRAM_MAX_LENGTH
        ):
            raise InvalidTelegramError()

        for character in self.value:
            if not character.isalnum() and character != "_":
                raise InvalidTelegramError()
