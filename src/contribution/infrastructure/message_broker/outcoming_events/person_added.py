import json
from dataclasses import dataclass

from contribution.domain import AddPersonContributionId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class OutcomingPersonAddedEvent:
    correlation_id: OperationId
    contribution_id: AddPersonContributionId

    def to_json(self) -> str:
        event_as_dict = {
            "correlation_id": self.correlation_id.hex,
            "contribution_id": self.contribution_id.hex,
        }
        return json.dumps(event_as_dict)
