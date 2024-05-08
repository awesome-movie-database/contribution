from typing import Protocol, Optional, Sequence
from datetime import date, datetime

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    AddMovieContributionId,
    UserId,
    Country,
    Money,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    PhotoUrl,
)


class OnMovieAdded(Protocol):
    async def __call__(
        self,
        *,
        id: AddMovieContributionId,
        author_id: UserId,
        eng_title: str,
        original_title: str,
        release_date: date,
        countries: Sequence[Country],
        genres: Sequence[Genre],
        mpaa: MPAA,
        duration: int,
        budget: Optional[Money],
        revenue: Optional[Money],
        roles: Sequence[ContributionRole],
        writers: Sequence[ContributionWriter],
        crew: Sequence[ContributionCrewMember],
        photos: Sequence[PhotoUrl],
        added_at: datetime,
    ) -> None:
        raise NotImplementedError
