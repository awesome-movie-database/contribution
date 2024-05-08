from contribution.domain.exceptions import (
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
)


MOVIE_ENG_TITLE_MIN_LENGTH = 1
MOVIE_ENG_TITLE_MAX_LENGTH = 128

MOVIE_ORIGINAL_TITLE_MIN_LENGTH = 1
MOVIE_ORIGINAL_TITLE_MAX_LENGTH = 128

MIN_MOVIE_DURATION = 1


class ValidateMovieEngTitle:
    def __call__(self, eng_title: str) -> None:
        eng_title_length = len(eng_title)

        if (
            eng_title_length < MOVIE_ENG_TITLE_MIN_LENGTH
            or eng_title_length > MOVIE_ENG_TITLE_MAX_LENGTH
        ):
            raise InvalidMovieEngTitleError()


class ValidateMovieOriginalTitle:
    def __call__(self, original_title: str) -> None:
        original_title_length = len(original_title)

        if (
            original_title_length < MOVIE_ORIGINAL_TITLE_MIN_LENGTH
            or original_title_length > MOVIE_ORIGINAL_TITLE_MAX_LENGTH
        ):
            raise InvalidMovieOriginalTitleError()


class ValidateMovieDuration:
    def __call__(self, duration: int) -> None:
        if duration < MIN_MOVIE_DURATION:
            raise InvalidMovieDurationError()
