from typing import Iterable

from uuid_extensions import uuid7

from contribution.domain import (
    RoleId,
    ContributionRole,
    ValidateRoleCharacter,
    ValidateRoleImportance,
)
from contribution.application.common.value_objects import MovieRole


class CreateContributionRoles:
    def __init__(
        self,
        validate_role_character: ValidateRoleCharacter,
        validate_role_importance: ValidateRoleImportance,
    ):
        self._validate_role_character = validate_role_character
        self._validate_role_importance = validate_role_importance

    def __call__(
        self,
        movie_roles: Iterable[MovieRole],
    ) -> list[ContributionRole]:
        contribution_roles = []
        for movie_role in movie_roles:
            contribution_role = self._create_contribution_role(movie_role)
            contribution_roles.append(contribution_role)

        return contribution_roles

    def _create_contribution_role(
        self,
        movie_role: MovieRole,
    ) -> ContributionRole:
        self._validate_role_character(movie_role.character)
        self._validate_role_importance(movie_role.importance)

        return ContributionRole(
            id=RoleId(uuid7()),
            person_id=movie_role.person_id,
            character=movie_role.character,
            importance=movie_role.importance,
            is_spoiler=movie_role.is_spoiler,
        )
