from dataclasses import dataclass
from typing import Iterable, Optional
from datetime import date

from contribution.domain import (
    Genre,
    MPAA,
    Country,
    Money,
    PhotoUrl,
)
from contribution.application.common import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
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
    roles: Iterable[MovieRole]
    writers: Iterable[MovieWriter]
    crew: Iterable[MovieCrewMember]
    photos: Iterable[PhotoUrl]
