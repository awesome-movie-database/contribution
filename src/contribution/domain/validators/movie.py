from contribution.domain.exceptions import (
    InvalidMovieTitleError,
    InvalidMovieDurationError,
)


MOVIE_TITLE_MIN_LENGTH = 1
MOVIE_TITLE_MAX_LENGTH = 128

MIN_MOVIE_DURATION = 1


class ValidateMovieTitle:
    def __call__(self, title: str) -> None:
        title_length = len(title)

        if (
            title_length < MOVIE_TITLE_MIN_LENGTH
            or title_length > MOVIE_TITLE_MAX_LENGTH
        ):
            raise InvalidMovieTitleError()


class ValidateMovieDuration:
    def __call__(self, duration: int) -> None:
        if duration < MIN_MOVIE_DURATION:
            raise InvalidMovieDurationError()
