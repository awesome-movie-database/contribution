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
