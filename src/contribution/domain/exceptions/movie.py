from .base import DomainError


class InvalidMovieEngTitleError(DomainError):
    ...


class InvalidMovieOriginalTitleError(DomainError):
    ...


class InvalidMovieSummaryError(DomainError):
    ...


class InvalidMovieDescriptionError(DomainError):
    ...


class InvalidMovieDurationError(DomainError):
    ...
