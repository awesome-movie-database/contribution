from dataclasses import dataclass

from contribution.domain import EditMovieContributionId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class IncomingEditMovieContributionRejectedEvent:
    operation_id: OperationId
    contribution_id: EditMovieContributionId
