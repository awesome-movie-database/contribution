from dataclasses import dataclass

from contribution.domain import (
    Writing,
    WriterId,
    PersonId,
)


@dataclass(frozen=True, slots=True)
class MovieWriter:
    id: WriterId
    person_id: PersonId
    writing: Writing
