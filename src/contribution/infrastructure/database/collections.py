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
    "PermissionsCollection",
    "user_collection_factory",
    "movie_collection_factory",
    "person_collection_factory",
    "role_collection_factory",
    "writer_collection_factory",
    "crew_member_collection_factory",
    "add_movie_contribution_collection_factory",
    "edit_movie_contribution_collection_factory",
    "add_person_contribution_collection_factory",
    "edit_person_contribution_collection_factory",
    "achievement_collection_factory",
    "permissions_collection_factory",
)

from typing import NewType

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


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
PermissionsCollection = NewType(
    "PermissionsCollection",
    AsyncIOMotorCollection,
)


def user_collection_factory(
    database: AsyncIOMotorDatabase,
) -> UserCollection:
    return database.get_collection("users")


def movie_collection_factory(
    database: AsyncIOMotorDatabase,
) -> MovieCollection:
    return database.get_collection("movies")


def person_collection_factory(
    database: AsyncIOMotorDatabase,
) -> PersonCollection:
    return database.get_collection("persons")


def role_collection_factory(
    database: AsyncIOMotorDatabase,
) -> RoleCollection:
    return database.get_collection("roles")


def writer_collection_factory(
    database: AsyncIOMotorDatabase,
) -> WriterCollection:
    return database.get_collection("writers")


def crew_member_collection_factory(
    database: AsyncIOMotorDatabase,
) -> CrewMemberCollection:
    return database.get_collection("crew_members")


def add_movie_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> AddMovieContributionCollection:
    return database.get_collection("add_movie_contributions")


def edit_movie_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> EditMovieContributionCollection:
    return database.get_collection("edit_movie_contributions")


def add_person_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> AddPersonContributionCollection:
    return database.get_collection("add_person_contributions")


def edit_person_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> EditPersonContributionCollection:
    return database.get_collection("edit_person_contributions")


def achievement_collection_factory(
    database: AsyncIOMotorDatabase,
) -> AchievementCollection:
    return database.get_collection("achievements")


def permissions_collection_factory(
    database: AsyncIOMotorDatabase,
) -> PermissionsCollection:
    return database.get_collection("permissions")
