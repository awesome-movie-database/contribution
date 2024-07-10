from typing import Optional

from contribution.domain import RoleId, Role


class RoleMap:
    def __init__(self):
        self._roles: list[Role] = list()

    def by_id(self, id: RoleId) -> Optional[Role]:
        for role in self._roles:
            if role.id == id:
                return role
        return None

    def save(self, role: Role) -> None:
        """
        Saves role in identity map if role doesn't
        exist, otherwise raises ValueError.
        """
        role_from_map = self.by_id(role.id)
        if role_from_map:
            message = "Role already exists in identity map"
            raise ValueError(message)
        self._roles.append(role)
