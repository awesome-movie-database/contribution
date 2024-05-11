from typing_extensions import TypedDict, Required
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
    countries: Sequence[Country]
    genres: Sequence[Genre]
    mpaa: MPAA
    duration: int
    budget: Optional[Money]
    revenue: Optional[Money]
    add_roles: Sequence[ContributionRole]
    remove_roles: Sequence[RoleId]
    add_writers: Sequence[ContributionWriter]
    remove_writers: Sequence[WriterId]
    add_crew: Sequence[ContributionCrewMember]
    remove_crew: Sequence[CrewMemberId]
