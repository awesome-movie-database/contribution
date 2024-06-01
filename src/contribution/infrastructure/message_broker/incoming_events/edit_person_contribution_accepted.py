from dataclasses import dataclass

from contribution.domain import EditPersonContributionId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingEditPersonContributionAcceptedEvent:
    correlation_id: CorrelationId
    contribution_id: EditPersonContributionId
