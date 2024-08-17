from contribution.domain.exceptions import (
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieSummaryError,
    InvalidMovieDescriptionError,
    InvalidMovieDurationError,
)


MOVIE_ENG_TITLE_MIN_LENGTH = 1
MOVIE_ENG_TITLE_MAX_LENGTH = 128

MOVIE_ORIGINAL_TITLE_MIN_LENGTH = 1
MOVIE_ORIGINAL_TITLE_MAX_LENGTH = 128

MOVIE_SUMMARY_MIN_LENGTH = 5
MOVIE_SUMMARY_MAX_LENGTH = 128

MOVIE_DESCRIPTION_MIN_LENGTH = 32
MOVIE_DESCRIPTION_MAX_LENGTH = 512

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


class ValidateMovieSummary:
    def __call__(self, summary: str) -> None:
        summary_length = len(summary)

        if (
            summary_length < MOVIE_SUMMARY_MIN_LENGTH
            or summary_length > MOVIE_SUMMARY_MAX_LENGTH
        ):
            raise InvalidMovieSummaryError()


class ValidateMovieDescription:
    def __call__(self, description: str) -> None:
        description_length = len(description)

        if (
            description_length < MOVIE_DESCRIPTION_MIN_LENGTH
            or description_length > MOVIE_DESCRIPTION_MAX_LENGTH
        ):
            raise InvalidMovieDescriptionError()


class ValidateMovieDuration:
    def __call__(self, duration: int) -> None:
        if duration < MIN_MOVIE_DURATION:
            raise InvalidMovieDurationError()
