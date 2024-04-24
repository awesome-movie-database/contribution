from dataclasses import dataclass
from typing import Optional
from datetime import date

from contribution.domain.value_objects import PersonId


@dataclass(slots=True)
class Person:
    id: PersonId
    name: str
    last_name: str
    birth_date: date
    death_date: Optional[date]
