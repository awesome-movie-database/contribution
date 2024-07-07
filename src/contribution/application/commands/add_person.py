from dataclasses import dataclass
from typing import Iterable, Optional
from datetime import date

from contribution.domain import Sex, PhotoUrl


@dataclass(frozen=True, slots=True)
class AddPersonCommand:
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
    photos: Iterable[PhotoUrl]
