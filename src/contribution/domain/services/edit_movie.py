from typing import Iterable, Optional
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
    PhotoUrl,
)
from contribution.domain.validators import (
    ValidateMovieEngTitle,
    ValidateMovieOriginalTitle,
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
        id: EditMovieContributionId,
        author: User,
        movie: Movie,
        eng_title: Maybe[str],
        original_title: Maybe[str],
        release_date: Maybe[date],
        countries: Maybe[Iterable[Country]],
        genres: Maybe[Iterable[Genre]],
        mpaa: Maybe[MPAA],
        duration: Maybe[int],
        budget: Maybe[Optional[Money]],
        revenue: Maybe[Optional[Money]],
        add_roles: Iterable[ContributionRole],
        remove_roles: Iterable[RoleId],
        add_writers: Iterable[ContributionWriter],
        remove_writers: Iterable[WriterId],
        add_crew: Iterable[ContributionCrewMember],
        remove_crew: Iterable[CrewMemberId],
        photos_to_add: Iterable[PhotoUrl],
        current_timestamp: datetime,
    ) -> EditMovieContribution:
        if not author.is_active:
            raise UserIsNotActiveError()

        if eng_title.is_set:
            self._validate_eng_title(eng_title.value)
        if original_title.is_set:
            self._validate_original_title(original_title.value)
        if duration.is_set:
            self._validate_duration(duration.value)

        self._ensure_contribution_does_not_duplicate_movie_fields_values(
            movie=movie,
            eng_title=eng_title,
            original_title=original_title,
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
            eng_title=eng_title,
            original_title=original_title,
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
            photos_to_add=photos_to_add,
            status=ContributionStatus.PENDING,
            created_at=current_timestamp,
            status_updated_at=None,
        )

    def _ensure_contribution_does_not_duplicate_movie_fields_values(
        self,
        *,
        movie: Movie,
        eng_title: Maybe[str],
        original_title: Maybe[str],
        release_date: Maybe[date],
        countries: Maybe[Iterable[Country]],
        genres: Maybe[Iterable[Genre]],
        mpaa: Maybe[MPAA],
        duration: Maybe[int],
        budget: Maybe[Optional[Money]],
        revenue: Maybe[Optional[Money]],
    ) -> None:
        fields_with_duplicates = []

        if eng_title.is_set and eng_title.value == movie.eng_title:
            fields_with_duplicates.append("eng_title")
        if (
            original_title.is_set
            and original_title.value == movie.original_title
        ):
            fields_with_duplicates.append("original_title")
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
