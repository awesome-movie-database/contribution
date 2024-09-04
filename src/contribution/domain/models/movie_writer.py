from dataclasses import dataclass

from contribution.domain.constants import Writing
from contribution.domain.value_objects import WriterId, PersonId


@dataclass(frozen=True, slots=True)
class MovieWriter:
    id: WriterId
    person_id: PersonId
    writing: Writing
