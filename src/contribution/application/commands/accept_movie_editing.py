from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from contribution.domain.value_objects import EditMovieContributionId
from contribution.application.common.value_objects import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
)


@dataclass(frozen=True, slots=True)
class AcceptMovieEditingCommand:
    contribution_id: EditMovieContributionId
    accepted_at: datetime
    add_roles: Sequence[MovieRole]
    add_writers: Sequence[MovieWriter]
    add_crew: Sequence[MovieCrewMember]
