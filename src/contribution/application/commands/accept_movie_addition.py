from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from contribution.domain import (
    AddMovieContributionId,
    MovieId,
)
from contribution.application.common import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
)


@dataclass(frozen=True, slots=True)
class AcceptMovieAdditionCommand:
    contribution_id: AddMovieContributionId
    movie_id: MovieId
    accepted_at: datetime
    roles: Sequence[MovieRole]
    writers: Sequence[MovieWriter]
    crew: Sequence[MovieCrewMember]
