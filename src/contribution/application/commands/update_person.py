from dataclasses import dataclass
from typing import Optional
from datetime import date

from contribution.domain import (
    Sex,
    PersonId,
    Maybe,
)


@dataclass(frozen=True, slots=True)
class UpdatePersonCommand:
    person_id: PersonId
    first_name: Maybe[str]
    last_name: Maybe[str]
    sex: Maybe[Sex]
    birth_date: Maybe[date]
    death_date: Maybe[Optional[date]]
