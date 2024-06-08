from dataclasses import dataclass

from contribution.domain import AddMovieContributionId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class IncomingAddMovieContributionRejectedEvent:
    operation_id: OperationId
    contribution_id: AddMovieContributionId
