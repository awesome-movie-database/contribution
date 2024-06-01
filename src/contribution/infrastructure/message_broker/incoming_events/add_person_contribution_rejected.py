from dataclasses import dataclass

from contribution.domain import AddPersonContributionId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingAddPersonContributionRejectedEvent:
    correlation_id: CorrelationId
    contribution_id: AddPersonContributionId
