from typing import Optional, Sequence
from dataclasses import dataclass
from datetime import date

from contribution.domain.constants import Sex
from contribution.domain.value_objects import (
    EditPersonContributionId,
    UserId,
    PersonId,
    PhotoUrl,
)
from contribution.domain.maybe import Maybe
from .contribution import Contribution


@dataclass(slots=True, unsafe_hash=True)
class EditPersonContribution(Contribution):
    id: EditPersonContributionId
    author_id: UserId
    person_id: PersonId
    first_name: Maybe[str]
    last_name: Maybe[str]
    sex: Maybe[Sex]
    birth_date: Maybe[date]
    death_date: Maybe[Optional[date]]
    add_photos: Sequence[PhotoUrl]
