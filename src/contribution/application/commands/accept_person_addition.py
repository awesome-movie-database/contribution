from dataclasses import dataclass

from contribution.domain.value_objects import (
    AddPersonContributionId,
    PersonId,
)


@dataclass(frozen=True, slots=True)
class AcceptPersonAdditionCommand:
    contribution_id: AddPersonContributionId
    person_id: PersonId
