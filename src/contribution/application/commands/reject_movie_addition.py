from dataclasses import dataclass

from contribution.domain.value_objects import AddMovieContributionId


@dataclass(frozen=True, slots=True)
class RejectMovieAdditionCommand:
    contribution_id: AddMovieContributionId
