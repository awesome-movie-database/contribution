import json
from dataclasses import dataclass

from contribution.domain import AchievementId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class OutcomingAchievementEarnedEvent:
    operation_id: OperationId
    achievement_id: AchievementId

    def to_json(self) -> str:
        event_as_dict = {
            "operation_id": self.operation_id.hex,
            "achievement_id": self.achievement_id.hex,
        }
        return json.dumps(event_as_dict)
