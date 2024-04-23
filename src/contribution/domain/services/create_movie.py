from typing import Sequence, Optional
from datetime import date

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    MovieId,
    Country,
    Money,
)
from contribution.domain.validators import (
    ValidateMovieTitle,
    ValidateMovieDuration,
)
from contribution.domain.entities import Movie


class CreateMovie:
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
        id: MovieId,
        title: str,
        release_date: date,
        countries: Sequence[Country],
        genres: Sequence[Genre],
        mpaa: MPAA,
        duration: int,
        budget: Optional[Money],
        revenue: Optional[Money],
    ) -> None:
        self._validate_title(title)
        self._validate_duration(duration)

        return Movie(
            id=id,
            title=title,
            release_date=release_date,
            countries=countries,
            genres=genres,
            mpaa=mpaa,
            duration=duration,
            budget=budget,
            revenue=revenue,
        )
