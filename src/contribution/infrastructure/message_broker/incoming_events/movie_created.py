from dataclasses import dataclass

from contribution.domain import MovieId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingMovieCreatedEvent:
    correlation_id: CorrelationId
    movie_id: MovieId
