# Fuck pydantic
# mypy: disable-error-code="assignment"

from typing import Optional
from datetime import date

from pydantic import BaseModel

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
from contribution.application import EditMovieCommand


class EditMovieRequest(BaseModel):
    movie_id: MovieId
    eng_title: str = None
    original_title: str = None
    release_date: date = None
    countries: list[Country] = None
    genres: list[Genre] = None
    mpaa: MPAA = None
    duration: int = None
    budget: Optional[Money] = None
    revenue: Optional[Money] = None
    add_roles: list[ContributionRole]
    remove_roles: list[RoleId]
    add_writers: list[ContributionWriter]
    remove_writers: list[WriterId]
    add_crew: list[ContributionCrewMember]
    remove_crew: list[CrewMemberId]
    photos_to_add: list[PhotoUrl]

    def to_command(self) -> EditMovieCommand:
        request_as_dict = self.model_dump(exclude_unset=True)

        eng_title = Maybe[str].from_mapping_by_key(
            mapping=request_as_dict,
            key="eng_title",
        )
        original_title = Maybe[str].from_mapping_by_key(
            mapping=request_as_dict,
            key="original_title",
        )
        release_date = Maybe[date].from_mapping_by_key(
            mapping=request_as_dict,
            key="release_date",
        )
        countries = Maybe[list[Country]].from_mapping_by_key(
            mapping=request_as_dict,
            key="countries",
        )
        genres = Maybe[list[Genre]].from_mapping_by_key(
            mapping=request_as_dict,
            key="genres",
        )
        mpaa = Maybe[MPAA].from_mapping_by_key(
            mapping=request_as_dict,
            key="mpaa",
        )
        duration = Maybe[int].from_mapping_by_key(
            mapping=request_as_dict,
            key="duration",
        )
        budget = Maybe[Optional[Money]].from_mapping_by_key(
            mapping=request_as_dict,
            key="budget",
        )
        revenue = Maybe[Optional[Money]].from_mapping_by_key(
            mapping=request_as_dict,
            key="revenue",
        )

        return EditMovieCommand(
            movie_id=self.movie_id,
            eng_title=eng_title,
            original_title=original_title,
            release_date=release_date,
            countries=countries,
            genres=genres,
            mpaa=mpaa,
            duration=duration,
            budget=budget,
            revenue=revenue,
            add_roles=self.add_roles,
            remove_roles=self.remove_roles,
            add_writers=self.add_writers,
            remove_writers=self.remove_writers,
            add_crew=self.add_crew,
            remove_crew=self.remove_crew,
            photos_to_add=self.photos_to_add,
        )
