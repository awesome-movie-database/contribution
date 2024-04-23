from typing import Sequence, Optional
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
    ValidateMovieTitle,
    ValidateMovieDuration,
)
from contribution.domain.entities import Movie
from contribution.domain.maybe import Maybe


class UpdateMovie:
    def __init__(
        self,
        validate_title: ValidateMovieTitle,
        valudate_duration: ValidateMovieDuration,
    ):
        self._validate_title = validate_title
        self._validate_duration = valudate_duration

    def __call__(
        self,
        movie: Movie,
        *,
        title: Maybe[str],
        release_date: Maybe[date],
        countries: Maybe[Sequence[Country]],
        genres: Maybe[Sequence[Genre]],
        mpaa: Maybe[MPAA],
        duration: Maybe[int],
        budget: Maybe[Optional[Money]],
        revenue: Maybe[Optional[Money]],
    ) -> None:
        if title.is_set:
            self._validate_title(title)
            movie.title = title.value
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
            self._validate_duration(duration)
            movie.duration = duration.value
