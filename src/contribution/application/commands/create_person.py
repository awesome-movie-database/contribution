from dataclasses import dataclass
from datetime import date
from typing import Optional

from contribution.domain import Sex, PersonId


@dataclass(frozen=True, slots=True)
class CreatePersonCommand:
    id: PersonId
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
