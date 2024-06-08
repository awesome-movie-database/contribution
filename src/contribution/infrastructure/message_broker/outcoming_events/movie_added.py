import json
from dataclasses import dataclass

from contribution.domain import AddMovieContributionId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class OutcomingMovieAddedEvent:
    operation_id: OperationId
    contribution_id: AddMovieContributionId

    def to_json(self) -> str:
        event_as_dict = {
            "operation_id": self.operation_id.hex,
            "contribution_id": self.contribution_id.hex,
        }
        return json.dumps(event_as_dict)
