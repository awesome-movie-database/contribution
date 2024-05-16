from typing import Optional

from contribution.domain import RoleId, Role


class RoleMap:
    def __init__(self):
        self._roles: set[Role] = set()

    def with_id(self, id: RoleId) -> Optional[Role]:
        for role in self._roles:
            if role.id == id:
                return role
        return None

    def save(self, role: Role) -> None:
        """
        Saves role in identity map if role doesn't
        exist, otherwise raises ValueError.
        """
        role_from_map = self.with_id(role.id)
        if role_from_map:
            message = "Role already exists in identity map"
            raise ValueError(message)
        self._roles.add(role)

    def update(self, role: Role) -> None:
        """
        Updates role in identity map if role exists,
        otherwise raises ValueError.
        """
        role_from_map = self.with_id(role.id)
        if not role_from_map:
            message = "Role doesn't exist in identity map"
            raise ValueError(message)
        self._roles.remove(role_from_map)
        self._roles.add(role)
