from dataclasses import dataclass
from typing import Generic, TypeVar

from contribution.domain.value_objects import (
    AddMovieContributionId,
    EditMovieContributionId,
    AddPersonContributionId,
    EditPersonContributionId,
)


T = TypeVar(
    "T",
    AddMovieContributionId,
    EditMovieContributionId,
    AddPersonContributionId,
    EditPersonContributionId,
)


@dataclass(frozen=True, slots=True)
class AcceptContributionCommand(Generic[T]):
    contribution_id: T
