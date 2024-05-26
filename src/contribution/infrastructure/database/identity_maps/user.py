from dataclasses import dataclass
from typing import Optional

from contribution.domain import UserId, User


@dataclass(slots=True, unsafe_hash=True)
class UserMapUnit:
    user: User
    is_acquired: bool


class UserMap:
    def __init__(self):
        self._units: set[UserMapUnit] = set()

    def with_id(self, id: UserId) -> Optional[User]:
        for unit in self._units:
            if unit.user.id == id:
                return unit.user
        return None

    def with_name(self, name: str) -> Optional[User]:
        for unit in self._units:
            if unit.user.name == name:
                return unit.user
        return None

    def with_email(self, email: str) -> Optional[User]:
        for unit in self._units:
            if unit.user.email == email:
                return unit.user
        return None

    def with_telegram(self, telegram: str) -> Optional[User]:
        for unit in self._units:
            if unit.user.telegram == telegram:
                return unit.user
        return None

    def save(self, user: User) -> None:
        """
        Saves user in identity map if user doesn't
        exist, otherwise raises ValueError.
        """
        user_from_map = self.with_id(user.id)
        if user_from_map:
            message = "User already exists in identity map"
            raise ValueError(message)

        unit = UserMapUnit(user=user, is_acquired=False)
        self._units.add(unit)

    def save_acquired(self, user: User) -> None:
        """
        Saves user as acquired in identity map if user
        doesn't exist or already exist and not marked as
        acquired, otherwise raises ValueError.
        """
        user_from_map = self.with_id(user.id)
        if not user_from_map:
            unit = UserMapUnit(user=user, is_acquired=True)
            self._units.add(unit)

        user_is_acquired = self.is_acquired(user)
        if user_is_acquired:
            message = (
                "User already exists in identity map and marked as acquired"
            )
            raise ValueError(message)

        for unit in self._units:
            if unit.user == user:
                unit.is_acquired = True
                return

    def is_acquired(self, user: User) -> bool:
        """
        Returns whether user is acquired if user exists
        in identity map, otherwise raises ValueError.
        """
        for unit in self._units:
            if unit.user == user:
                return unit.is_acquired
        message = "User doesn't exist in identity map"
        raise ValueError(message)
