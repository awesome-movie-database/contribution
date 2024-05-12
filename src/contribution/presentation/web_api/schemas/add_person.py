from dataclasses import dataclass
from typing import Optional
from datetime import date

from contribution.domain.constants import Sex


@dataclass(frozen=True, slots=True)
class AddPersonSchema:
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
