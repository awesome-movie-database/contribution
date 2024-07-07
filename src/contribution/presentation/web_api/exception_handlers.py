from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse

from contribution.domain import (
    UserIsNotActiveError,
    InvalidMovieEngTitleError,
    InvalidMovieOriginalTitleError,
    InvalidMovieDurationError,
    InvalidPersonFirstNameError,
    InvalidPersonLastNameError,
    InvalidPersonBirthOrDeathDateError,
)
from contribution.application import (
    UserDoesNotExistError,
    NotEnoughPermissionsError,
    PersonsDoNotExistError,
    MovieDoesNotExistError,
    RolesDoNotExistError,
    WritersDoNotExistError,
    CrewMembersDoNotExistError,
    PersonDoesNotExistError,
)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserIsNotActiveError,
        _on_user_is_not_active_error,
    )
    app.add_exception_handler(
        InvalidMovieEngTitleError,
        _on_invalid_movie_eng_title_error,
    )
    app.add_exception_handler(
        InvalidMovieOriginalTitleError,
        _on_invalid_movie_original_title_error,
    )
    app.add_exception_handler(
        InvalidMovieDurationError,
        _on_invalid_movie_duration_error,
    )
    app.add_exception_handler(
        InvalidPersonFirstNameError,
        _on_invalid_person_first_name_error,
    )
    app.add_exception_handler(
        InvalidPersonLastNameError,
        _on_invalid_person_last_name_error,
    )
    app.add_exception_handler(
        InvalidPersonBirthOrDeathDateError,
        _on_invalid_person_birth_or_death_date_error,
    )
    app.add_exception_handler(
        UserDoesNotExistError,
        _on_user_does_not_exist_error,
    )
    app.add_exception_handler(
        NotEnoughPermissionsError,
        _on_not_enough_permissions_error,
    )
    app.add_exception_handler(
        PersonsDoNotExistError,
        _on_persons_do_not_exist_error,
    )
    app.add_exception_handler(
        MovieDoesNotExistError,
        _on_movie_does_not_exist_error,
    )
    app.add_exception_handler(
        RolesDoNotExistError,
        _on_roles_do_not_exist_error,
    )
    app.add_exception_handler(
        WritersDoNotExistError,
        _on_writers_do_not_exist_error,
    )
    app.add_exception_handler(
        CrewMembersDoNotExistError,
        _on_crew_members_do_not_exist_error,
    )
    app.add_exception_handler(
        PersonDoesNotExistError,
        _on_person_does_not_exist_error,
    )
    app.add_exception_handler(Exception, _on_unknown_error)


def _on_user_is_not_active_error(*_) -> JSONResponse:
    return JSONResponse(content="User is not active.", status_code=400)


def _on_invalid_movie_eng_title_error(*_) -> JSONResponse:
    return JSONResponse(
        content=(
            "Invalid length of eng_title. Lenght of eng_title must be "
            "more than 1 character and less than 128 characters."
        ),
        status_code=400,
    )


def _on_invalid_movie_original_title_error(*_) -> JSONResponse:
    return JSONResponse(
        content=(
            "Invalid length of original_title. Lenght of original_title "
            "must be more than 1 character and less than 128 characters."
        ),
        status_code=400,
    )


def _on_invalid_movie_duration_error(*_) -> JSONResponse:
    return JSONResponse(
        content=("Invalid duration. Duration must be more than 1 minute. "),
        status_code=400,
    )


def _on_invalid_person_first_name_error(*_) -> JSONResponse:
    return JSONResponse(
        content=(
            "Invalid length of first_name. Lenght of first_name must be "
            "more than 1 character and less than 128 characters."
        ),
        status_code=400,
    )


def _on_invalid_person_last_name_error(*_) -> JSONResponse:
    return JSONResponse(
        content=(
            "Invalid length of last_name. Lenght of last_name must be "
            "more than 1 character and less than 128 characters."
        ),
        status_code=400,
    )


def _on_invalid_person_birth_or_death_date_error(*_) -> JSONResponse:
    return JSONResponse(
        content=(
            "Invalid birth_date or death_date. Date of death must be "
            "later than date of birth. "
        ),
        status_code=400,
    )


def _on_user_does_not_exist_error(*_) -> Response:
    return Response(status_code=500)


def _on_not_enough_permissions_error(*_) -> JSONResponse:
    return JSONResponse(
        content="User has not enough permissions.",
        status_code=400,
    )


def _on_persons_do_not_exist_error(
    _,
    error: PersonsDoNotExistError,
) -> JSONResponse:
    return JSONResponse(
        content=(
            "Some of persons do not exist. "
            f"Ids of non existing persons: {error.ids_of_missing_persons}"
        ),
        status_code=400,
    )


def _on_movie_does_not_exist_error(*_) -> JSONResponse:
    return JSONResponse(content="Movie doesn't exist.", status_code=400)


def _on_roles_do_not_exist_error(
    _,
    error: RolesDoNotExistError,
) -> JSONResponse:
    return JSONResponse(
        content=(
            "Some of roles do not exist. "
            f"Ids of non existing roles: {error.ids_of_missing_roles}"
        ),
        status_code=400,
    )


def _on_writers_do_not_exist_error(
    _,
    error: WritersDoNotExistError,
) -> JSONResponse:
    return JSONResponse(
        content=(
            "Some of writers do not exist. "
            f"Ids of non existing writers: {error.ids_of_missing_writers}"
        ),
        status_code=400,
    )


def _on_crew_members_do_not_exist_error(
    _,
    error: CrewMembersDoNotExistError,
) -> JSONResponse:
    return JSONResponse(
        content=(
            "Some of crew members do not exist. Ids of non "
            f"existing crew members: {error.ids_of_missing_crew_members}"
        ),
        status_code=400,
    )


def _on_person_does_not_exist_error(*_) -> JSONResponse:
    return JSONResponse(content="Person doesn't exist.", status_code=400)


def _on_unknown_error(*_) -> Response:
    return Response(status_code=500)
