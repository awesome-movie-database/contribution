from contribution.domain.constants import ContributionStatus

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Contribution:
    status: ContributionStatus
    created_at: datetime
    status_updated_at: Optional[datetime]
