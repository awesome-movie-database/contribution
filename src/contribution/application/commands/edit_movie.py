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
    add_roles: Iterable[ContributionRole]
    remove_roles: Collection[RoleId]
    add_writers: Iterable[ContributionWriter]
    remove_writers: Collection[WriterId]
    add_crew: Iterable[ContributionCrewMember]
    remove_crew: Collection[CrewMemberId]
    add_photos: Iterable[PhotoUrl]
