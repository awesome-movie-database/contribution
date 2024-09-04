from typing import Iterable, Optional
from dataclasses import dataclass
from datetime import date

from contribution.domain.constants import Sex
from contribution.domain.value_objects import (
    EditPersonContributionId,
    UserId,
    PersonId,
)
from contribution.domain.maybe import Maybe
from .photo_url import PhotoUrl
from .contribution import Contribution


@dataclass(slots=True)
class EditPersonContribution(Contribution):
    id: EditPersonContributionId
    author_id: UserId
    person_id: PersonId
    first_name: Maybe[str]
    last_name: Maybe[str]
    sex: Maybe[Sex]
    birth_date: Maybe[date]
    death_date: Maybe[Optional[date]]
    photos_to_add: Iterable[PhotoUrl]
