from typing import Iterable, Optional
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
    ValidateMovieSummary,
    ValidateMovieDescription,
    ValidateMovieDuration,
)
from contribution.domain.entities import Movie


class CreateMovie:
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
        *,
        id: MovieId,
        eng_title: str,
        original_title: str,
        summary: str,
        description: str,
        release_date: date,
        countries: Iterable[Country],
        genres: Iterable[Genre],
        mpaa: MPAA,
        duration: int,
        budget: Optional[Money],
        revenue: Optional[Money],
    ) -> Movie:
        self._validate_eng_title(eng_title)
        self._validate_original_title(original_title)
        self._validate_summary(summary)
        self._validate_description(description)
        self._validate_duration(duration)

        return Movie(
            id=id,
            eng_title=eng_title,
            original_title=original_title,
            summary=summary,
            description=description,
            release_date=release_date,
            countries=countries,
            genres=genres,
            mpaa=mpaa,
            duration=duration,
            budget=budget,
            revenue=revenue,
        )
