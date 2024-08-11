from typing import Annotated, Optional
from datetime import date

import rich
import rich.prompt
import rich.table
from cyclopts import Parameter

from contribution.domain import (
    MPAA,
    Genre,
    MovieId,
    RoleId,
    WriterId,
    CrewMemberId,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    Country,
    Money,
    Maybe,
)
from contribution.application import (
    CommandProcessor,
    UpdateMovieCommand,
)
from contribution.infrastructure import cli_ioc_container_factory
from contribution.presentation.cli.converters import (
    str_to_uuid,
    strs_to_uuids,
    int_to_maybe_int,
    str_to_maybe_str,
    str_to_maybe_date,
    countries_to_maybe_countries,
    strs_to_maybe_genres,
    str_to_maybe_mpaa,
    json_to_maybe_optional_money,
    jsons_to_movie_roles,
    jsons_to_movie_writers,
    jsons_to_movie_crew,
)


async def update_movie(
    id: Annotated[
        MovieId,
        Parameter(
            "--id",
            converter=str_to_uuid,
            help="Id in [bright_yellow]UUID[/bright_yellow] format.",
        ),
    ],
    eng_title: Annotated[
        Maybe[str],
        Parameter("--eng-title", converter=str_to_maybe_str),
    ] = Maybe[str].without_value(),
    original_title: Annotated[
        Maybe[str],
        Parameter("--original-title", converter=str_to_maybe_str),
    ] = Maybe[str].without_value(),
    release_date: Annotated[
        Maybe[date],
        Parameter(
            "--release-date",
            converter=str_to_maybe_date,
            help=(
                "Release date in [bright_green]ISO 8601[/bright_green] format."
            ),
        ),
    ] = Maybe[date].without_value(),
    countries: Annotated[
        Maybe[list[Country]],
        Parameter(
            "--countries",
            converter=countries_to_maybe_countries,
            help=(
                "Countries in [bright_green]ISO 3166 alpha 2"
                "[/bright_green] format."
            ),
        ),
    ] = Maybe[list[Country]].without_value(),
    genres: Annotated[
        Maybe[list[Genre]],
        Parameter("--genres", converter=strs_to_maybe_genres),
    ] = Maybe[list[Genre]].without_value(),
    mpaa: Annotated[
        Maybe[MPAA],
        Parameter("--mpaa", converter=str_to_maybe_mpaa),
    ] = Maybe[MPAA].without_value(),
    duration: Annotated[
        Maybe[int],
        Parameter("--duration", converter=int_to_maybe_int),
    ] = Maybe[int].without_value(),
    budget: Annotated[
        Maybe[Optional[Money]],
        Parameter(
            "--budget",
            converter=json_to_maybe_optional_money,
            show_default=True,
            help=(
                "Budget in [bright_red]json[/bright_red] format.\n\n"
                "Example:\n"
                "[bright_red]{\n"
                '    "amount": "100",\n'
                '    "currency": "USD"\n'
                "}[/bright_red]"
            ),
        ),
    ] = Maybe[Optional[Money]].without_value(),
    revenue: Annotated[
        Maybe[Optional[Money]],
        Parameter(
            "--revenue",
            converter=json_to_maybe_optional_money,
            show_default=True,
            help=(
                "Revenue in [bright_red]json[/bright_red] format.\n\n"
                "Example:\n"
                "[bright_red]{\n"
                '    "amount": "100",\n'
                '    "currency": "USD"\n'
                "}[/bright_red]"
            ),
        ),
    ] = Maybe[Optional[Money]].without_value(),
    roles_to_add: Annotated[
        Optional[list[MovieRole]],
        Parameter(
            "--roles-to-add",
            converter=jsons_to_movie_roles,
            help=(
                "Roles in [bright_red]json[/bright_red] format "
                "(Each role must be in [bright_red]json[/bright_red] "
                "format).\n\n"
                "Example of a role:\n"
                "[bright_red]{\n"
                '    "id": "066746d0-a236-7f1d-8000-1711de4b4e03",\n'
                '    "person_id": "066746c5-fda5-7985-8000-d16c225a8b17",\n'
                '    "character": "Captain Jack Sparrow",\n'
                '    "importance": 1,\n'
                '    "is_spoiler": false\n'
                "}[/bright_red]"
            ),
        ),
    ] = None,
    roles_to_remove: Annotated[
        Optional[list[RoleId]],
        Parameter(
            "--roles-to-remove",
            converter=strs_to_uuids,
            help=(
                "Role ids in [bright_yellow]UUID[/bright_yellow] format "
                "(Each writer id must be in [bright_yellow]UUID"
                "[/bright_yellow] format)."
            ),
        ),
    ] = None,
    writers_to_add: Annotated[
        Optional[list[MovieWriter]],
        Parameter(
            "--writers-to-add",
            converter=jsons_to_movie_writers,
            help=(
                "Writers in [bright_red]json[/bright_red] format "
                "(Each writer must be in [bright_red]json[/bright_red] "
                "format).\n\n"
                "Example of a writer:\n"
                "[bright_red]{\n"
                '    "id": "066746e6-b9b3-7b13-8000-120c5b23f268",\n'
                '    "person_id": "066746e5-71e3-73e5-8000-d9bdd5ead582",\n'
                '    "writing": "Origin"\n'
                "}[/bright_red]"
            ),
        ),
    ] = None,
    writers_to_remove: Annotated[
        Optional[list[WriterId]],
        Parameter(
            "--writers-to-remove",
            converter=strs_to_uuids,
            help=(
                "Writer ids in [bright_yellow]UUID[/bright_yellow] format "
                "(Each writer id must be in [bright_yellow]UUID"
                "[/bright_yellow] format)."
            ),
        ),
    ] = None,
    crew_to_add: Annotated[
        Optional[list[MovieCrewMember]],
        Parameter(
            "--crew-to-add",
            converter=jsons_to_movie_crew,
            help=(
                "Crew members in [bright_red]json[/bright_red] format "
                "(Each crew member must be in [bright_red]json[/bright_red] "
                "format).\n\n"
                "Example of a crew member:\n"
                "[bright_red]{\n"
                '   "id": "066746ff-367e-721f-8000-655eca7fdf18",\n'
                '   "person_id": "066746fe-49a6-7e8d-8000-d780471a81f9",\n'
                '   "membership": "Director"\n'
                "}[/bright_red]"
            ),
        ),
    ] = None,
    crew_to_remove: Annotated[
        Optional[list[CrewMemberId]],
        Parameter(
            "--crew-to-remove",
            converter=strs_to_uuids,
            help=(
                "Crew member ids in [bright_yellow]UUID[/bright_yellow] "
                "format (Each writer id must be in [bright_yellow]UUID"
                "[/bright_yellow] format)."
            ),
        ),
    ] = None,
) -> None:
    """
    Updates a movie. Does not notify other services about it.
    Asks confirmation before execting.
    """
    executing_is_confirmed = rich.prompt.Confirm.ask(
        "You are going to update a movie.\n"
        "This action does not notify other services about updates.\n"
        "Would you like to continue?",
    )
    if not executing_is_confirmed:
        return

    ioc_container = cli_ioc_container_factory()

    command = UpdateMovieCommand(
        movie_id=id,
        eng_title=eng_title,
        original_title=original_title,
        release_date=release_date,
        countries=countries,
        genres=genres,
        mpaa=mpaa,
        duration=duration,
        budget=budget,
        revenue=revenue,
        roles_to_add=roles_to_add or [],
        roles_to_remove=roles_to_remove or [],
        writers_to_add=writers_to_add or [],
        writers_to_remove=writers_to_remove or [],
        crew_to_add=crew_to_add or [],
        crew_to_remove=crew_to_remove or [],
    )
    async with ioc_container() as ioc_container_request:
        command_processor = await ioc_container_request.get(
            CommandProcessor[UpdateMovieCommand, None],
        )
        await command_processor.process(command)

    updated_movie_fields_table = _update_movie_fields_table_factory(
        id=id,
        eng_title=eng_title,
        original_title=original_title,
        release_date=release_date,
        countries=countries,
        genres=genres,
        mpaa=mpaa,
        duration=duration,
        budget=budget,
        revenue=revenue,
        roles_to_add=roles_to_add,
        roles_to_remove=roles_to_remove,
        writers_to_add=writers_to_add,
        writers_to_remove=writers_to_remove,
        crew_to_add=crew_to_add,
        crew_to_remove=crew_to_remove,
    )

    rich.print("Movie has been updated successfully")
    rich.print(updated_movie_fields_table)


def _update_movie_fields_table_factory(
    *,
    id: MovieId,
    eng_title: Maybe[str],
    original_title: Maybe[str],
    release_date: Maybe[date],
    countries: Maybe[list[Country]],
    genres: Maybe[list[Genre]],
    mpaa: Maybe[MPAA],
    duration: Maybe[int],
    budget: Maybe[Optional[Money]],
    revenue: Maybe[Optional[Money]],
    roles_to_add: Optional[list[MovieRole]],
    roles_to_remove: Optional[list[RoleId]],
    writers_to_add: Optional[list[MovieWriter]],
    writers_to_remove: Optional[list[WriterId]],
    crew_to_add: Optional[list[MovieCrewMember]],
    crew_to_remove: Optional[list[CrewMemberId]],
) -> rich.table.Table:
    updated_movie_fields_table = rich.table.Table(
        "id",
        title="Updated movie fields",
    )
    update_movie_field_values = [str(id)]

    if eng_title.is_set:
        updated_movie_fields_table.add_column("eng_title")
        update_movie_field_values.append(eng_title.value)
    if original_title.is_set:
        updated_movie_fields_table.add_column("original_title")
        update_movie_field_values.append(original_title.value)
    if release_date.is_set:
        updated_movie_fields_table.add_column("release_date")
        update_movie_field_values.append(release_date.value.isoformat())
    if countries.is_set:
        updated_movie_fields_table.add_column("countries")
        update_movie_field_values.append(str(countries.value))
    if genres.is_set:
        updated_movie_fields_table.add_column("genres")
        update_movie_field_values.append(str(genres.value))
    if mpaa.is_set:
        updated_movie_fields_table.add_column("mpaa")
        update_movie_field_values.append(mpaa.value)
    if duration.is_set:
        updated_movie_fields_table.add_column("duration")
        update_movie_field_values.append(str(duration.value))
    if budget.is_set:
        budget_ = budget.value
        updated_movie_fields_table.add_column("budget")
        update_movie_field_values.append(str(budget_) if budget_ else "None")
    if revenue.is_set:
        revenue_ = revenue.value
        updated_movie_fields_table.add_column("revenue")
        update_movie_field_values.append(str(revenue_) if revenue_ else "None")
    if roles_to_add:
        updated_movie_fields_table.add_column("added_roles")
        update_movie_field_values.append(str(roles_to_add))
    if roles_to_remove:
        updated_movie_fields_table.add_column("removed_role_ids")
        update_movie_field_values.append(str(roles_to_remove))
    if writers_to_add:
        updated_movie_fields_table.add_column("added_writers")
        update_movie_field_values.append(str(writers_to_add))
    if writers_to_remove:
        updated_movie_fields_table.add_column("removed_writer_ids")
        update_movie_field_values.append(str(writers_to_remove))
    if crew_to_add:
        updated_movie_fields_table.add_column("added_crew")
        update_movie_field_values.append(str(crew_to_add))
    if crew_to_remove:
        updated_movie_fields_table.add_column("removed_crew_member_ids")
        update_movie_field_values.append(str(crew_to_remove))

    updated_movie_fields_table.add_row(*update_movie_field_values)

    return updated_movie_fields_table
