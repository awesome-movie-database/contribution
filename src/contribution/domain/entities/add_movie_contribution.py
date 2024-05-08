from typing import Sequence, Optional
from dataclasses import dataclass
from datetime import date

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    AddMovieContributionId,
    UserId,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    Country,
    Money,
    PhotoUrl,
)
from .contribution import Contribution


@dataclass(slots=True)
class AddMovieContribution(Contribution):
    id: AddMovieContributionId
    author_id: UserId
    eng_title: str
    original_title: str
    release_date: date
    countries: Sequence[Country]
    genres: Sequence[Genre]
    mpaa: MPAA
    duration: int
    budget: Optional[Money]
    revenue: Optional[Money]
    roles: Sequence[ContributionRole]
    writers: Sequence[ContributionWriter]
    crew: Sequence[ContributionCrewMember]
    photos: Sequence[PhotoUrl]
