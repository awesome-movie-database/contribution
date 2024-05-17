from typing import (
    Collection,
    Iterable,
    Optional,
    TypedDict,
    Required,
)
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
)


class EditMovieSchema(TypedDict, total=False):
    movie_id: Required[MovieId]
    eng_title: str
    original_title: str
    release_date: date
    countries: Iterable[Country]
    genres: Iterable[Genre]
    mpaa: MPAA
    duration: int
    budget: Optional[Money]
    revenue: Optional[Money]
    add_roles: Iterable[ContributionRole]
    remove_roles: Collection[RoleId]
    add_writers: Iterable[ContributionWriter]
    remove_writers: Collection[WriterId]
    add_crew: Iterable[ContributionCrewMember]
    remove_crew: Collection[CrewMemberId]
