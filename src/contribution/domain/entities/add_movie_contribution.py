from typing import Sequence, Optional
from dataclasses import dataclass
from datetime import date, datetime

from contribution.domain.constants import (
    Genre,
    MPAA,
    ContributionStatus,
)
from contribution.domain.value_objects import (
    AddMovieContributionId,
    UserId,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    Country,
    Money,
)


@dataclass(slots=True)
class AddMovieContribution:
    id: AddMovieContributionId
    author_id: UserId
    title: str
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
    status: ContributionStatus
    created_at: datetime
    updated_at: Optional[datetime]
