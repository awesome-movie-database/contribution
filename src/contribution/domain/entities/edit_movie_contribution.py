from typing import Iterable, Optional
from dataclasses import dataclass
from datetime import date

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    EditMovieContributionId,
    UserId,
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
)
from contribution.domain.maybe import Maybe
from .contribution import Contribution


@dataclass(slots=True)
class EditMovieContribution(Contribution):
    id: EditMovieContributionId
    author_id: UserId
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
    remove_roles: Iterable[RoleId]
    add_writers: Iterable[ContributionWriter]
    remove_writers: Iterable[WriterId]
    add_crew: Iterable[ContributionCrewMember]
    remove_crew: Iterable[CrewMemberId]
    photos_to_add: Iterable[PhotoUrl]
