from dataclasses import dataclass

from contribution.domain import AddPersonContributionId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class IncomingAddPersonContributionRejectedEvent:
    operation_id: OperationId
    contribution_id: AddPersonContributionId
