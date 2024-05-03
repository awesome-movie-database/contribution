from dataclasses import dataclass
from datetime import datetime

from contribution.domain.value_objects import (
    AddMovieContributionId,
    MovieId,
)


@dataclass(frozen=True, slots=True)
class AcceptMovieAdditionCommand:
    contribution_id: AddMovieContributionId
    movie_id: MovieId
    accepted_at: datetime
