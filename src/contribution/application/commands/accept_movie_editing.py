from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from contribution.domain import EditMovieContributionId
from contribution.application.common import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
)


@dataclass(frozen=True, slots=True)
class AcceptMovieEditingCommand:
    contribution_id: EditMovieContributionId
    accepted_at: datetime
    roles_to_add: Iterable[MovieRole]
    writers_to_add: Iterable[MovieWriter]
    crew_to_add: Iterable[MovieCrewMember]
