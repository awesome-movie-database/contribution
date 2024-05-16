from typing import Optional

from contribution.domain import (
    UserId,
    Email,
    Telegram,
    User,
)


class UserMap:
    def __init__(self):
        self._users: set[User] = set()

    def with_id(self, id: UserId) -> Optional[User]:
        for user in self._users:
            if user.id == id:
                return user
        return None

    def with_name(self, name: str) -> Optional[User]:
        for user in self._users:
            if user.name == name:
                return user
        return None

    def with_email(self, email: Email) -> Optional[User]:
        for user in self._users:
            if user.email == email:
                return user
        return None

    def with_telegram(self, telegram: Telegram) -> Optional[User]:
        for user in self._users:
            if user.telegram == telegram:
                return user
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
        self._users.add(user)

    def update(self, user: User) -> None:
        """
        Updates user in identity map if user exists,
        otherwise raises ValueError.
        """
        user_from_map = self.with_id(user.id)
        if not user_from_map:
            message = "User doesn't exist in identity map"
            raise ValueError(message)
        self._users.remove(user_from_map)
        self._users.add(user)
