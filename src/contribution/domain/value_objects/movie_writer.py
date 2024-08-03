from dataclasses import dataclass

from contribution.domain.constants import Writing
from .writer_id import WriterId
from .person_id import PersonId


@dataclass(frozen=True, slots=True)
class MovieWriter:
    id: WriterId
    person_id: PersonId
    writing: Writing
