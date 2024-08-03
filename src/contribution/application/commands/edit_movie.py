from dataclasses import dataclass
from typing import Collection, Iterable, Optional
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
    PhotoUrl,
    Maybe,
)
from contribution.application.common import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
)


@dataclass(frozen=True, slots=True)
class EditMovieCommand:
    movie_id: MovieId
    eng_title: Maybe[str]
    original_title: Maybe[str]
    release_date: Maybe[date]
    countries: Maybe[Iterable[Country]]
    genres: Maybe[Iterable[Genre]]
    mpaa: Maybe[MPAA]
    duration: Maybe[int]
    budget: Maybe[Optional[Money]]
    revenue: Maybe[Optional[Money]]
    roles_to_add: Iterable[MovieRole]
    roles_to_remove: Collection[RoleId]
    writers_to_add: Iterable[MovieWriter]
    writers_to_remove: Collection[WriterId]
    crew_to_add: Iterable[MovieCrewMember]
    crew_to_remove: Collection[CrewMemberId]
    photos_to_add: Iterable[PhotoUrl]
