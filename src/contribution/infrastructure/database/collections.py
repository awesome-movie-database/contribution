# mypy: disable-error-code="valid-newtype"

__all__ = (
    "UserCollection",
    "MovieCollection",
    "PersonCollection",
    "RoleCollection",
    "WriterCollection",
    "CrewMemberCollection",
    "AddMovieContributionCollection",
    "EditMovieContributionCollection",
    "AddPersonContributionCollection",
    "EditPersonContributionCollection",
    "AchievementCollection",
)

from typing import NewType

from motor.motor_asyncio import AsyncIOMotorCollection


UserCollection = NewType("UserCollection", AsyncIOMotorCollection)
MovieCollection = NewType("MovieCollection", AsyncIOMotorCollection)
PersonCollection = NewType("PersonCollection", AsyncIOMotorCollection)
RoleCollection = NewType("RoleCollection", AsyncIOMotorCollection)
WriterCollection = NewType("WriterCollection", AsyncIOMotorCollection)
CrewMemberCollection = NewType("CrewMemberCollection", AsyncIOMotorCollection)
AddMovieContributionCollection = NewType(
    "AddMovieContributionCollection",
    AsyncIOMotorCollection,
)
EditMovieContributionCollection = NewType(
    "EditMovieContributionCollection",
    AsyncIOMotorCollection,
)
AddPersonContributionCollection = NewType(
    "AddPersonContributionCollection",
    AsyncIOMotorCollection,
)
EditPersonContributionCollection = NewType(
    "EditPersonContributionCollection",
    AsyncIOMotorCollection,
)
AchievementCollection = NewType(
    "AchievementCollection",
    AsyncIOMotorCollection,
)
