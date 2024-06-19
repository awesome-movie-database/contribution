import json
from typing import Any, Annotated, Iterable, Optional
from datetime import date

from cyclopts import Parameter
from adaptix import Retort

from contribution.domain import (
    MPAA,
    Genre,
    Country,
    Money,
    MovieId,
)
from contribution.application import (
    CommandProcessor,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    CreateMovieCommand,
)
from contribution.infrastructure import ioc_container_factory


async def create_movie(
    id: Annotated[MovieId, Parameter("--id")],
    eng_title: Annotated[str, Parameter("--eng-title")],
    original_title: Annotated[str, Parameter("--original-title")],
    release_date: Annotated[date, Parameter("--release-date")],
    countries: Annotated[Iterable[Country], Parameter("--countries")],
    genres: Annotated[Iterable[Genre], Parameter("--genres")],
    mpaa: Annotated[MPAA, Parameter("--mpaa")],
    duration: Annotated[int, Parameter("--duration")],
    budget: Annotated[Optional[str], Parameter("--budget")] = None,
    revenue: Annotated[Optional[str], Parameter("--revenue")] = None,
    roles: Annotated[list[str], Parameter("--roles")] = [],
    writers: Annotated[list[str], Parameter("--writers")] = [],
    crew: Annotated[list[str], Parameter("--crew")] = [],
) -> None:
    ioc_container = ioc_container_factory()
    converter = Converter()

    command = CreateMovieCommand(
        id=id,
        eng_title=eng_title,
        original_title=original_title,
        release_date=release_date,
        countries=countries,
        genres=genres,
        mpaa=mpaa,
        duration=duration,
        budget=(converter.json_string_to_money(budget) if budget else None),
        revenue=(converter.json_string_to_money(revenue) if revenue else None),
        roles=converter.json_strings_to_roles(roles),
        writers=converter.json_strings_to_writers(writers),
        crew=converter.json_strings_to_crew(crew),
    )
    command_processor = await ioc_container.get(
        CommandProcessor[CreateMovieCommand, None],
    )
    await command_processor.process(command)

    print("Movie has been added successfully")


class Converter:
    def __init__(self):
        self._retort = Retort()

    def json_string_to_money(self, json_: str) -> Money:
        money_as_dict = self._money_as_json_to_dict(json_)
        money = self._retort.load(money_as_dict, Money)
        return money

    def json_strings_to_roles(
        self,
        jsons_: Iterable[str],
    ) -> list[MovieRole]:
        roles_as_dicts = self._roles_as_jsons_to_dicts(jsons_)
        roles = self._retort.load(roles_as_dicts, list[MovieRole])
        return roles

    def json_strings_to_writers(
        self,
        jsons_: Iterable[str],
    ) -> list[MovieWriter]:
        writers_as_dicts = self._writers_as_jsons_to_dicts(jsons_)
        writers = self._retort.load(writers_as_dicts, list[MovieRole])
        return writers

    def json_strings_to_crew(
        self,
        jsons_: Iterable[str],
    ) -> list[MovieCrewMember]:
        crew_as_dicts = self._crew_as_jsons_to_dicts(jsons_)
        crew = self._retort.load(crew_as_dicts, list[MovieRole])
        return crew

    def _money_as_json_to_dict(self, money_as_json: str) -> dict:
        money_as_dict = self._ensure_dict(json.loads(money_as_json))
        return money_as_dict

    def _roles_as_jsons_to_dicts(
        self,
        roles_as_jsons: Iterable[str],
    ) -> list[dict]:
        roles_as_dicts = []
        for role_as_json in roles_as_jsons:
            role_as_dict = self._ensure_dict(json.loads(role_as_json))
            roles_as_dicts.append(role_as_dict)
        return roles_as_dicts

    def _writers_as_jsons_to_dicts(
        self,
        writers_as_jsons: Iterable[str],
    ) -> list[dict]:
        writers_as_dicts = []
        for writer_as_json in writers_as_jsons:
            writer_as_dict = self._ensure_dict(json.loads(writer_as_json))
            writers_as_dicts.append(writer_as_dict)
        return writers_as_dicts

    def _crew_as_jsons_to_dicts(
        self,
        crew_as_jsons: Iterable[str],
    ) -> list[dict]:
        crew_as_dicts = []
        for crew_member_as_json in crew_as_jsons:
            crew_member_as_dict = self._ensure_dict(
                json.loads(crew_member_as_json),
            )
            crew_as_dicts.append(crew_member_as_dict)
        return crew_as_dicts

    def _ensure_dict(self, maybe_dict: Any) -> dict:
        if not isinstance(maybe_dict, dict):
            raise ValueError()
        return maybe_dict
