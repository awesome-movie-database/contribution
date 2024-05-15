from dataclasses import dataclass
from typing import Optional, Sequence
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
    added_at: datetime
