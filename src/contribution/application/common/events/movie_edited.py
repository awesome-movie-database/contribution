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
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
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
    add_photos: Iterable[PhotoUrl]
    edited_at: datetime
