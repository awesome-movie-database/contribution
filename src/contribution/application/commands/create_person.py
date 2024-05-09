from dataclasses import dataclass
from datetime import date
from typing import Optional

from contribution.domain.constants import Sex
from contribution.domain.value_objects import PersonId


@dataclass(frozen=True, slots=True)
class CreatePersonCommand:
    id: PersonId
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
