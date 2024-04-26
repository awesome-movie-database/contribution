from typing import Sequence, Optional
from datetime import date, datetime

from contribution.domain.constants import (
    Genre,
    MPAA,
    ContributionStatus,
)
from contribution.domain.value_objects import (
    AddMovieContributionId,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    Country,
    Money,
)
from contribution.domain.validators import (
    ValidateMovieTitle,
    ValidateMovieDuration,
)
from contribution.domain.exceptions import UserIsNotActiveError
from contribution.domain.entities import (
    AddMovieContribution,
    User,
)


class AddMovie:
    def __init__(
        self,
        validate_title: ValidateMovieTitle,
        valudate_duration: ValidateMovieDuration,
    ):
        self._validate_title = validate_title
        self._validate_duration = valudate_duration

    def __call__(
        self,
        *,
        id: AddMovieContributionId,
        author: User,
        title: str,
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
        current_timestamp: datetime,
    ) -> AddMovieContribution:
        if not author.is_active:
            raise UserIsNotActiveError()

        self._validate_title(title)
        self._validate_duration(duration)

        return AddMovieContribution(
            id=id,
            author_id=author.id,
            title=title,
            release_date=release_date,
            countries=countries,
            genres=genres,
            mpaa=mpaa,
            duration=duration,
            budget=budget,
            revenue=revenue,
            roles=roles,
            writers=writers,
            crew=crew,
            status=ContributionStatus.PENDING,
            created_at=current_timestamp,
            status_updated_at=None,
        )
