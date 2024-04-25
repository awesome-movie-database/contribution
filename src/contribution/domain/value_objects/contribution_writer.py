from dataclasses import dataclass

from contribution.domain.constants import Writing
from contribution.domain.value_objects import PersonId


@dataclass(frozen=True, slots=True)
class ContributionWriter:
    person_id: PersonId
    writing: Writing
