from dataclasses import dataclass
from typing import Iterable, Optional
from datetime import date, datetime

from contribution.domain import (
    Genre,
    MPAA,
    EditMovieContributionId,
    UserId,
    MovieId,
    RoleId,
    WriterId,
    CrewMemberId,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    Country,
    Money,
    PhotoUrl,
    Maybe,
)


@dataclass(frozen=True, slots=True)
class MovieEditedEvent:
    contribution_id: EditMovieContributionId
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
    edited_at: datetime
