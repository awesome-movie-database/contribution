from dataclasses import dataclass

from contribution.domain import AddMovieContributionId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingAddMovieContributionRejectedEvent:
    correlation_id: CorrelationId
    contribution_id: AddMovieContributionId
