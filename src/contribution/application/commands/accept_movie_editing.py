from dataclasses import dataclass

from contribution.domain.value_objects import EditMovieContributionId


@dataclass(frozen=True, slots=True)
class AcceptMovieEditingCommand:
    contribution_id: EditMovieContributionId
