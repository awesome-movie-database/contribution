from dataclasses import dataclass
from typing import Iterable, Optional
from datetime import date

from contribution.domain import (
    Genre,
    MPAA,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    Country,
    Money,
    PhotoUrl,
)


@dataclass(frozen=True, slots=True)
class AddMovieCommand:
    eng_title: str
    original_title: str
    release_date: date
    countries: Iterable[Country]
    genres: Iterable[Genre]
    mpaa: MPAA
    duration: int
    budget: Optional[Money]
    revenue: Optional[Money]
    roles: Iterable[ContributionRole]
    writers: Iterable[ContributionWriter]
    crew: Iterable[ContributionCrewMember]
    photos: Iterable[PhotoUrl]
