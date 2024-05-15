from dataclasses import dataclass
from typing import Sequence, Optional
from datetime import date

from contribution.domain import (
    Genre,
    MPAA,
    MovieId,
    RoleId,
    WriterId,
    CrewMemberId,
    Country,
    Money,
    Maybe,
)
from contribution.application.common import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
)


@dataclass(frozen=True, slots=True)
class UpdateMovieCommand:
    movie_id: MovieId
    eng_title: Maybe[str]
    original_title: Maybe[str]
    release_date: Maybe[date]
    countries: Maybe[Sequence[Country]]
    genres: Maybe[Sequence[Genre]]
    mpaa: Maybe[MPAA]
    duration: Maybe[int]
    budget: Maybe[Optional[Money]]
    revenue: Maybe[Optional[Money]]
    add_roles: Sequence[MovieRole]
    remove_roles: Sequence[RoleId]
    add_writers: Sequence[MovieWriter]
    remove_writers: Sequence[WriterId]
    add_crew: Sequence[MovieCrewMember]
    remove_crew: Sequence[CrewMemberId]
