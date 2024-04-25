from typing import Sequence, Optional
from datetime import date, datetime

from contribution.domain.constants import (
    Genre,
    MPAA,
    ContributionStatus,
)
from contribution.domain.value_objects import (
    EditMovieContributionId,
    RoleId,
    WriterId,
    CrewMemberId,
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
from contribution.domain.exceptions import (
    UserIsNotActiveError,
    ContributionDataDuplicationError,
)
from contribution.domain.entities import (
    EditMovieContribution,
    Movie,
    User,
)
from contribution.domain.maybe import Maybe


class EditMovie:
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
        id: EditMovieContributionId,
        author: User,
        movie: Movie,
        title: Maybe[str],
        release_date: Maybe[date],
        countries: Maybe[Sequence[Country]],
        genres: Maybe[Sequence[Genre]],
        mpaa: Maybe[MPAA],
        duration: Maybe[int],
        budget: Maybe[Optional[Money]],
        revenue: Maybe[Optional[Money]],
        add_roles: Sequence[ContributionRole],
        remove_roles: Sequence[RoleId],
        add_writers: Sequence[ContributionWriter],
        remove_writers: Sequence[WriterId],
        add_crew: Sequence[ContributionCrewMember],
        remove_crew: Sequence[CrewMemberId],
        current_timestamp: datetime,
    ) -> EditMovieContribution:
        if not author.is_active:
            raise UserIsNotActiveError()

        if title.is_set:
            self._validate_title(title.value)
        if duration.is_set:
            self._validate_duration(duration.value)

        self._ensure_contribution_does_not_duplicate_movie(
            movie=movie,
            title=title,
            release_date=release_date,
            countries=countries,
            genres=genres,
            mpaa=mpaa,
            duration=duration,
            budget=budget,
            revenue=revenue,
        )

        return EditMovieContribution(
            id=id,
            author_id=author.id,
            movie_id=movie.id,
            title=title,
            release_date=release_date,
            countries=countries,
            genres=genres,
            mpaa=mpaa,
            duration=duration,
            budget=budget,
            revenue=revenue,
            add_roles=add_roles,
            remove_roles=remove_roles,
            add_writers=add_writers,
            remove_writers=remove_writers,
            add_crew=add_crew,
            remove_crew=remove_crew,
            status=ContributionStatus.PENDING,
            created_at=current_timestamp,
            updated_at=None,
        )

    def _ensure_contribution_does_not_duplicate_movie(
        self,
        *,
        movie: Movie,
        title: Maybe[str],
        release_date: Maybe[date],
        countries: Maybe[Sequence[Country]],
        genres: Maybe[Sequence[Genre]],
        mpaa: Maybe[MPAA],
        duration: Maybe[int],
        budget: Maybe[Optional[Money]],
        revenue: Maybe[Optional[Money]],
    ) -> None:
        fields_with_duplicates = []

        if title.is_set and title.value == movie.title:
            fields_with_duplicates.append("title")
        if release_date.is_set and release_date.value == movie.release_date:
            fields_with_duplicates.append("release_date")
        if countries.is_set and countries.value == movie.countries:
            fields_with_duplicates.append("countries")
        if genres.is_set and genres.value == movie.genres:
            fields_with_duplicates.append("genres")
        if mpaa.is_set and mpaa.value == movie.mpaa:
            fields_with_duplicates.append("mpaa")
        if duration.is_set and duration.value == movie.duration:
            fields_with_duplicates.append("duration")
        if budget.is_set and budget.value == movie.budget:
            fields_with_duplicates.append("budget")
        if revenue.is_set and revenue.value == movie.revenue:
            fields_with_duplicates.append("revenue")

        if fields_with_duplicates:
            raise ContributionDataDuplicationError(fields_with_duplicates)
