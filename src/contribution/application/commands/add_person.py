from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import date

from contribution.domain import Sex


@dataclass(frozen=True, slots=True)
class AddPersonCommand:
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
    photos: Sequence[bytes]
