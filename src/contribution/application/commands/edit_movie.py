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
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    Country,
    Money,
    PhotoUrl,
    Maybe,
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
    roles_to_add: Iterable[ContributionRole]
    roles_to_remove: Collection[RoleId]
    writers_to_add: Iterable[ContributionWriter]
    writers_to_remove: Collection[WriterId]
    crew_to_add: Iterable[ContributionCrewMember]
    crew_to_remove: Collection[CrewMemberId]
    photos_to_add: Iterable[PhotoUrl]
