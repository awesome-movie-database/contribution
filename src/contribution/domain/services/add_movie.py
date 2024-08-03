from typing import Iterable, Optional
from datetime import date, datetime

from contribution.domain.constants import (
    Genre,
    MPAA,
    ContributionStatus,
)
from contribution.domain.value_objects import (
    AddMovieContributionId,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    Country,
    Money,
    PhotoUrl,
)
from contribution.domain.validators import (
    ValidateMovieEngTitle,
    ValidateMovieOriginalTitle,
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
        validate_eng_title: ValidateMovieEngTitle,
        validate_original_title: ValidateMovieOriginalTitle,
        valudate_duration: ValidateMovieDuration,
    ):
        self._validate_eng_title = validate_eng_title
        self._validate_original_title = validate_original_title
        self._validate_duration = valudate_duration

    def __call__(
        self,
        *,
        id: AddMovieContributionId,
        author: User,
        eng_title: str,
        original_title: str,
        release_date: date,
        countries: Iterable[Country],
        genres: Iterable[Genre],
        mpaa: MPAA,
        duration: int,
        budget: Optional[Money],
        revenue: Optional[Money],
        roles: Iterable[MovieRole],
        writers: Iterable[MovieWriter],
        crew: Iterable[MovieCrewMember],
        photos: Iterable[PhotoUrl],
        current_timestamp: datetime,
    ) -> AddMovieContribution:
        if not author.is_active:
            raise UserIsNotActiveError()

        self._validate_eng_title(eng_title)
        self._validate_original_title(original_title)
        self._validate_duration(duration)

        return AddMovieContribution(
            id=id,
            author_id=author.id,
            eng_title=eng_title,
            original_title=original_title,
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
            photos=photos,
            status_updated_at=None,
        )
