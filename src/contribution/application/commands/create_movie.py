from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import date

from contribution.domain import (
    Genre,
    MPAA,
    MovieId,
    Country,
    Money,
)
from contribution.application.common import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
)


@dataclass(frozen=True, slots=True)
class CreateMovieCommand:
    id: MovieId
    eng_title: str
    original_title: str
    release_date: date
    countries: Sequence[Country]
    genres: Sequence[Genre]
    mpaa: MPAA
    duration: int
    budget: Optional[Money]
    revenue: Optional[Money]
    roles: Sequence[MovieRole]
    writers: Sequence[MovieWriter]
    crew: Sequence[MovieCrewMember]
