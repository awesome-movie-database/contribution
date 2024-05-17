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
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    PhotoUrl,
)


@dataclass(frozen=True, slots=True)
class MovieAddedEvent:
    contribution_id: AddMovieContributionId
    author_id: UserId
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
    added_at: datetime
