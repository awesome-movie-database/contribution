from dataclasses import dataclass
from datetime import datetime

from contribution.domain import (
    AddMovieContributionId,
    MovieId,
)


@dataclass(frozen=True, slots=True)
class AcceptMovieAddingCommand:
    contribution_id: AddMovieContributionId
    movie_id: MovieId
    accepted_at: datetime
