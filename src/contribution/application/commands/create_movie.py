from dataclasses import dataclass
from typing import Iterable, Optional
from datetime import date

from contribution.domain import (
    Genre,
    MPAA,
    MovieId,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    Country,
    Money,
)


@dataclass(frozen=True, slots=True)
class CreateMovieCommand:
    id: MovieId
    eng_title: str
    original_title: str
    summary: str
    description: str
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
