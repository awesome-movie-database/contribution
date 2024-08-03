from dataclasses import dataclass

from contribution.domain import Writing, PersonId


@dataclass(frozen=True, slots=True)
class MovieWriter:
    person_id: PersonId
    writing: Writing
