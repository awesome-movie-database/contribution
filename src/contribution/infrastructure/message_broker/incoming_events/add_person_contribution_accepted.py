from dataclasses import dataclass

from contribution.domain import AddPersonContributionId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingAddPersonContributionAcceptedEvent:
    correlation_id: CorrelationId
    contribution_id: AddPersonContributionId
