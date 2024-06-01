import json
from dataclasses import dataclass

from contribution.domain import AddMovieContributionId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class OutcomingMovieAddedEvent:
    correlation_id: CorrelationId
    contribution_id: AddMovieContributionId

    def to_json(self) -> str:
        event_as_dict = {
            "correlation_id": self.correlation_id.hex,
            "contribution_id": self.contribution_id.hex,
        }
        return json.dumps(event_as_dict)
