from typing import Iterable

from uuid_extensions import uuid7

from contribution.domain import (
    RoleId,
    MovieRole,
    ValidateRoleCharacter,
    ValidateRoleImportance,
)
from contribution.application.common.value_objects import ContributionRole


class CreateMovieRoles:
    def __init__(
        self,
        validate_role_character: ValidateRoleCharacter,
        validate_role_importance: ValidateRoleImportance,
    ):
        self._validate_role_character = validate_role_character
        self._validate_role_importance = validate_role_importance

    def __call__(
        self,
        contribution_roles: Iterable[ContributionRole],
    ) -> list[MovieRole]:
        movie_roles = []
        for contribution_role in contribution_roles:
            self._validate_role_character(contribution_role.character)
            self._validate_role_importance(contribution_role.importance)

            movie_role = MovieRole(
                id=RoleId(uuid7()),
                person_id=contribution_role.person_id,
                character=contribution_role.character,
                importance=contribution_role.importance,
                is_spoiler=contribution_role.is_spoiler,
            )
            movie_roles.append(movie_role)

        return movie_roles
