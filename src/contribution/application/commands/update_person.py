from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import date

from contribution.domain.constants import Sex
from contribution.domain.value_objects import PersonId
from contribution.domain.maybe import Maybe


@dataclass(frozen=True, slots=True)
class UpdatePersonCommand:
    person_id: PersonId
    first_name: Maybe[str]
    last_name: Maybe[str]
    sex: Maybe[Sex]
    birth_date: Maybe[date]
    death_date: Maybe[Optional[date]]
    add_photos: Sequence[bytes]
