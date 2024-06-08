from dataclasses import dataclass

from contribution.domain import MovieId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class IncomingMovieUpdatedEvent:
    operation_id: OperationId
    movie_id: MovieId
