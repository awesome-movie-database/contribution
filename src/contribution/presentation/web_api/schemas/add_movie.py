from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import date

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    Country,
    Money,
)


@dataclass(frozen=True, slots=True)
class AddMovieSchema:
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
