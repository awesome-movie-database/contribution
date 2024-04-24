import re
from dataclasses import dataclass

from contribution.domain.exceptions import InvalidEmailError


PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        match = re.fullmatch(PATTERN, self.value)
        if not match:
            raise InvalidEmailError()
