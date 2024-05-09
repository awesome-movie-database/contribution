from dataclasses import dataclass
from typing import Sequence, Optional
from datetime import date

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    MovieId,
    RoleId,
    WriterId,
    CrewMemberId,
    Country,
    Money,
)
from contribution.domain.maybe import Maybe
from contribution.application.common.value_objects import (
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
