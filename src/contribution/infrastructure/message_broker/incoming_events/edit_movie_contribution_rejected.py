from dataclasses import dataclass

from contribution.domain import EditMovieContributionId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingEditMovieContributionRejectedEvent:
    correlation_id: CorrelationId
    contribution_id: EditMovieContributionId
