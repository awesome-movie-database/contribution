import json
from dataclasses import dataclass

from contribution.domain import AchievementId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class RealAchievementEarnedEvent:
    correlation_id: CorrelationId
    achievement_id: AchievementId

    def to_json(self) -> str:
        event_as_dict = {
            "correlation_id": self.correlation_id.hex,
            "achievement_id": self.achievement_id.hex,
        }
        return json.dumps(event_as_dict)
