from typing import Iterable, Optional
from datetime import date

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    Country,
    Money,
)
from contribution.domain.validators import (
    ValidateMovieEngTitle,
    ValidateMovieOriginalTitle,
    ValidateMovieSummary,
    ValidateMovieDescription,
    ValidateMovieDuration,
)
from contribution.domain.entities import Movie
from contribution.domain.maybe import Maybe


class UpdateMovie:
    def __init__(
        self,
        validate_eng_title: ValidateMovieEngTitle,
        validate_original_title: ValidateMovieOriginalTitle,
        validate_summary: ValidateMovieSummary,
        validate_description: ValidateMovieDescription,
        valudate_duration: ValidateMovieDuration,
    ):
        self._validate_eng_title = validate_eng_title
        self._validate_original_title = validate_original_title
        self._validate_summary = validate_summary
        self._validate_description = validate_description
        self._validate_duration = valudate_duration

    def __call__(
        self,
        movie: Movie,
        *,
        eng_title: Maybe[str],
        original_title: Maybe[str],
        summary: Maybe[str],
        description: Maybe[str],
        release_date: Maybe[date],
        countries: Maybe[Iterable[Country]],
        genres: Maybe[Iterable[Genre]],
        mpaa: Maybe[MPAA],
        duration: Maybe[int],
        budget: Maybe[Optional[Money]],
        revenue: Maybe[Optional[Money]],
    ) -> None:
        if eng_title.is_set:
            self._validate_eng_title(eng_title.value)
            movie.eng_title = eng_title.value
        if original_title.is_set:
            self._validate_original_title(original_title.value)
            movie.original_title = original_title.value
        if summary.is_set:
            self._validate_summary(summary.value)
            movie.summary = summary.value
        if description.is_set:
            self._validate_description(description.value)
            movie.description = description.value
        if release_date.is_set:
            movie.release_date = release_date.value
        if countries.is_set:
            movie.countries = countries.value
        if genres.is_set:
            movie.genres = genres.value
        if mpaa.is_set:
            movie.mpaa = mpaa.value
        if budget.is_set:
            movie.budget = budget.value
        if revenue.is_set:
            movie.revenue = revenue.value
        if duration.is_set:
            self._validate_duration(duration.value)
            movie.duration = duration.value
