__all__ = (
    "ApplicationError",
    "UserIdIsAlreadyTakenError",
    "UserNameIsAlreadyTakenError",
    "UserEmailIsAlreadyTakenError",
    "UserTelegramIsAlreadyTakenError",
    "UserDoesNotExistError",
    "MovieDoesNotExistError",
    "PersonDoesNotExistError",
    "PersonsDoNotExistError",
    "RolesDoNotExistError",
    "WritersDoNotExistError",
    "CrewMembersDoNotExistError",
    "NotEnoughPermissionsError",
)

from .base import ApplicationError
from .user import (
    UserIdIsAlreadyTakenError,
    UserNameIsAlreadyTakenError,
    UserEmailIsAlreadyTakenError,
    UserTelegramIsAlreadyTakenError,
    UserDoesNotExistError,
)
from .movie import MovieDoesNotExistError
from .person import (
    PersonDoesNotExistError,
    PersonsDoNotExistError,
)
from .role import RolesDoNotExistError
from .writer import WritersDoNotExistError
from .crew import CrewMembersDoNotExistError
from .permissions import NotEnoughPermissionsError
