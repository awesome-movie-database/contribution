from dataclasses import dataclass

from contribution.domain.constants import Writing
from .person_id import PersonId


@dataclass(frozen=True, slots=True)
class ContributionWriter:
    person_id: PersonId
    writing: Writing
