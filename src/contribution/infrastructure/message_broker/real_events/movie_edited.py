import json
from dataclasses import dataclass

from contribution.domain import EditMovieContributionId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class RealMovieEditedEvent:
    correlation_id: CorrelationId
    contribution_id: EditMovieContributionId

    def to_json(self) -> str:
        event_as_dict = {
            "correlation_id": self.correlation_id.hex,
            "contribution_id": self.contribution_id.hex,
        }
        return json.dumps(event_as_dict)
