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
    roles_to_add: Iterable[ContributionRole]
    roles_to_remove: Iterable[RoleId]
    writers_to_add: Iterable[ContributionWriter]
    writers_to_remove: Iterable[WriterId]
    crew_to_add: Iterable[ContributionCrewMember]
    crew_to_remove: Iterable[CrewMemberId]
    photos_to_add: Iterable[PhotoUrl]
