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
)
from .movie_role import MovieRole
from .movie_writer import MovieWriter
from .movie_crew_member import MovieCrewMember
from .country import Country
from .money import Money
from .photo_url import PhotoUrl
from contribution.domain.maybe import Maybe
from .contribution import Contribution


@dataclass(slots=True)
class EditMovieContribution(Contribution):
    id: EditMovieContributionId
    author_id: UserId
    movie_id: MovieId
    eng_title: Maybe[str]
    original_title: Maybe[str]
    summary: Maybe[str]
    description: Maybe[str]
    release_date: Maybe[date]
    countries: Maybe[Iterable[Country]]
    genres: Maybe[Iterable[Genre]]
    mpaa: Maybe[MPAA]
    duration: Maybe[int]
    budget: Maybe[Optional[Money]]
    revenue: Maybe[Optional[Money]]
    roles_to_add: Iterable[MovieRole]
    roles_to_remove: Iterable[RoleId]
    writers_to_add: Iterable[MovieWriter]
    writers_to_remove: Iterable[WriterId]
    crew_to_add: Iterable[MovieCrewMember]
    crew_to_remove: Iterable[CrewMemberId]
    photos_to_add: Iterable[PhotoUrl]
