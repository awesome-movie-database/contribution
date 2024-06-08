import json
from dataclasses import dataclass

from contribution.domain import EditMovieContributionId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class OutcomingMovieEditedEvent:
    operation_id: OperationId
    contribution_id: EditMovieContributionId

    def to_json(self) -> str:
        event_as_dict = {
            "operation_id": self.operation_id.hex,
            "contribution_id": self.contribution_id.hex,
        }
        return json.dumps(event_as_dict)
