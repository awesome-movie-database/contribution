from dataclasses import dataclass
from datetime import datetime

from contribution.domain.value_objects import AddPersonContributionId


@dataclass(frozen=True, slots=True)
class RejectPersonAdditionCommand:
    contribution_id: AddPersonContributionId
    rejected_at: datetime
