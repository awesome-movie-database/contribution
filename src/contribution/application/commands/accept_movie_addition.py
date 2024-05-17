from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

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
    roles: Iterable[MovieRole]
    writers: Iterable[MovieWriter]
    crew: Iterable[MovieCrewMember]
