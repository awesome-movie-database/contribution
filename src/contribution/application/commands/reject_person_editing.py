from dataclasses import dataclass
from datetime import datetime

from contribution.domain.value_objects import EditPersonContributionId


@dataclass(frozen=True, slots=True)
class RejectPersonEditingCommand:
    contribution_id: EditPersonContributionId
    rejected_at: datetime
