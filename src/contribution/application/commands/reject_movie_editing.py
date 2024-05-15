from dataclasses import dataclass
from datetime import datetime

from contribution.domain import EditMovieContributionId


@dataclass(frozen=True, slots=True)
class RejectMovieEditingCommand:
    contribution_id: EditMovieContributionId
    rejected_at: datetime
