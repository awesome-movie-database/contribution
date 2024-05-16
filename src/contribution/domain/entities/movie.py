from typing import Sequence, Optional
from dataclasses import dataclass
from datetime import date

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    MovieId,
    Country,
    Money,
)


@dataclass(slots=True, unsafe_hash=True)
class Movie:
    id: MovieId
    eng_title: str
    original_title: str
    release_date: date
    countries: Sequence[Country]
    genres: Sequence[Genre]
    mpaa: MPAA
    duration: int
    budget: Optional[Money]
    revenue: Optional[Money]
