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
    collection = database.get_collection("users")
    return UserCollection(collection)


def movie_collection_factory(
    database: AsyncIOMotorDatabase,
) -> MovieCollection:
    collection = database.get_collection("movies")
    return MovieCollection(collection)


def person_collection_factory(
    database: AsyncIOMotorDatabase,
) -> PersonCollection:
    collection = database.get_collection("persons")
    return PersonCollection(collection)


def role_collection_factory(
    database: AsyncIOMotorDatabase,
) -> RoleCollection:
    collection = database.get_collection("roles")
    return RoleCollection(collection)


def writer_collection_factory(
    database: AsyncIOMotorDatabase,
) -> WriterCollection:
    collection = database.get_collection("writers")
    return WriterCollection(collection)


def crew_member_collection_factory(
    database: AsyncIOMotorDatabase,
) -> CrewMemberCollection:
    collection = database.get_collection("crew_members")
    return CrewMemberCollection(collection)


def add_movie_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> AddMovieContributionCollection:
    collection = database.get_collection("add_movie_contributions")
    return AddMovieContributionCollection(collection)


def edit_movie_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> EditMovieContributionCollection:
    collection = database.get_collection("edit_movie_contributions")
    return EditMovieContributionCollection(collection)


def add_person_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> AddPersonContributionCollection:
    collection = database.get_collection("add_person_contributions")
    return AddPersonContributionCollection(collection)


def edit_person_contribution_collection_factory(
    database: AsyncIOMotorDatabase,
) -> EditPersonContributionCollection:
    collection = database.get_collection("edit_person_contributions")
    return EditPersonContributionCollection(collection)


def achievement_collection_factory(
    database: AsyncIOMotorDatabase,
) -> AchievementCollection:
    collection = database.get_collection("achievements")
    return AchievementCollection(collection)


def permissions_collection_factory(
    database: AsyncIOMotorDatabase,
) -> PermissionsCollection:
    collection = database.get_collection("permissions")
    return PermissionsCollection(collection)
