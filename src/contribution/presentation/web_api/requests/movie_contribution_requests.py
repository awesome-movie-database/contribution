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
    Country,
    Money,
    PhotoUrl,
    Maybe,
)
from contribution.application import (
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
    EditMovieCommand,
)


class EditMovieRequest(BaseModel):
    movie_id: MovieId
    eng_title: str = None
    original_title: str = None
    summary: str = None
    description: str = None
    release_date: date = None
    countries: list[Country] = None
    genres: list[Genre] = None
    mpaa: MPAA = None
    duration: int = None
    budget: Optional[Money] = None
    revenue: Optional[Money] = None
    roles_to_add: list[ContributionRole]
    roles_to_remove: list[RoleId]
    writers_to_add: list[ContributionWriter]
    writers_to_remove: list[WriterId]
    crew_to_add: list[ContributionCrewMember]
    crew_to_remove: list[CrewMemberId]
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
        summary = Maybe[str].from_mapping_by_key(
            mapping=request_as_dict,
            key="summary",
        )
        description = Maybe[str].from_mapping_by_key(
            mapping=request_as_dict,
            key="description",
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
            summary=summary,
            description=description,
            release_date=release_date,
            countries=countries,
            genres=genres,
            mpaa=mpaa,
            duration=duration,
            budget=budget,
            revenue=revenue,
            roles_to_add=self.roles_to_add,
            roles_to_remove=self.roles_to_remove,
            writers_to_add=self.writers_to_add,
            writers_to_remove=self.writers_to_remove,
            crew_to_add=self.crew_to_add,
            crew_to_remove=self.crew_to_remove,
            photos_to_add=self.photos_to_add,
        )
