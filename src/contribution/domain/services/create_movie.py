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
    ValidateMovieEngTitle,
    ValidateMovieOriginalTitle,
    ValidateMovieDuration,
)
from contribution.domain.entities import Movie


class CreateMovie:
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
        id: MovieId,
        eng_title: str,
        original_title: str,
        release_date: date,
        countries: Sequence[Country],
        genres: Sequence[Genre],
        mpaa: MPAA,
        duration: int,
        budget: Optional[Money],
        revenue: Optional[Money],
    ) -> Movie:
        self._validate_eng_title(eng_title)
        self._validate_original_title(original_title)
        self._validate_duration(duration)

        return Movie(
            id=id,
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
