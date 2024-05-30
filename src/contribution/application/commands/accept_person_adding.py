from dataclasses import dataclass
from datetime import datetime

from contribution.domain import (
    AddPersonContributionId,
    PersonId,
)


@dataclass(frozen=True, slots=True)
class AcceptPersonAddingCommand:
    contribution_id: AddPersonContributionId
    person_id: PersonId
    accepted_at: datetime
