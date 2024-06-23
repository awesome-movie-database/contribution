import json
from typing import Any

from adaptix import Retort

from contribution.domain import Money
from contribution.application import (
    MovieRole,
    MovieWriter,
    MovieCrewMember,
)
from contribution.presentation.cli.exceptions import ValueIsNotDictError


_retort = Retort()


def json_to_money(json_: str) -> Money:
    json_as_dict = _ensure_dict(json.loads(json_))
    money = _retort.load(json_as_dict, Money)
    return money


def jsons_to_movie_roles(jsons: str) -> list[MovieRole]:
    jsons_as_dicts = [_ensure_dict(json.loads(json_)) for json_ in jsons]
    movie_roles = _retort.load(jsons_as_dicts, list[MovieRole])
    return movie_roles


def jsons_to_movie_writers(jsons: str) -> list[MovieWriter]:
    jsons_as_dicts = [_ensure_dict(json.loads(json_)) for json_ in jsons]
    movie_writers = _retort.load(jsons_as_dicts, list[MovieWriter])
    return movie_writers


def jsons_to_movie_crew(jsons: str) -> list[MovieCrewMember]:
    jsons_as_dicts = [_ensure_dict(json.loads(json_)) for json_ in jsons]
    movie_crew = _retort.load(jsons_as_dicts, list[MovieCrewMember])
    return movie_crew


def _ensure_dict(value: Any) -> dict:
    """
    Returns dict if value is dict, otherwise
    raises ValueIsNotDictError.
    """
    if not isinstance(value, dict):
        raise ValueIsNotDictError(value)
    return value
