from dataclasses import dataclass
from datetime import datetime

from contribution.domain.value_objects import (
    AddPersonContributionId,
    PersonId,
)


@dataclass(frozen=True, slots=True)
class AcceptPersonAdditionCommand:
    contribution_id: AddPersonContributionId
    person_id: PersonId
    accepted_at: datetime