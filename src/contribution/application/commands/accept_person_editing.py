from dataclasses import dataclass
from datetime import datetime

from contribution.domain import EditPersonContributionId


@dataclass(frozen=True, slots=True)
class AcceptPersonEditingCommand:
    contribution_id: EditPersonContributionId
    accepted_at: datetime
