from dataclasses import dataclass
from typing import Iterable, Optional
from datetime import date, datetime

from contribution.domain import (
    Genre,
    MPAA,
    AddMovieContributionId,
    UserId,
    Country,
    Money,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    PhotoUrl,
)


@dataclass(frozen=True, slots=True)
class MovieAddedEvent:
    contribution_id: AddMovieContributionId
    author_id: UserId
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
    photos: Iterable[PhotoUrl]
    added_at: datetime
