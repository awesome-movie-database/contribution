from dataclasses import dataclass
from datetime import datetime

from contribution.domain import AddMovieContributionId


@dataclass(frozen=True, slots=True)
class RejectMovieAddingCommand:
    contribution_id: AddMovieContributionId
    rejected_at: datetime
