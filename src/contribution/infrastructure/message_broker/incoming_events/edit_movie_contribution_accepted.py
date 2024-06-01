from dataclasses import dataclass

from contribution.domain import EditMovieContributionId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingEditMovieContributionAcceptedEvent:
    correlation_id: CorrelationId
    contribution_id: EditMovieContributionId
