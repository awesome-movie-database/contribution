from dishka import Provider, Scope
from motor.motor_asyncio import AsyncIOMotorDatabase

from contribution.infrastructure.database import (
    UserCollection,
    MovieCollection,
    PersonCollection,
    RoleCollection,
    WriterCollection,
    CrewMemberCollection,
    AddMovieContributionCollection,
    EditMovieContributionCollection,
    AddPersonContributionCollection,
    EditPersonContributionCollection,
    AchievementCollection,
)


def collections_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(user_collection_factory)
    provider.provide(movie_collection_factory)
    provider.provide(person_collection_factory)
    provider.provide(role_collection_factory)
    provider.provide(writer_collection_factory)
    provider.provide(crew_member_collection_factory)
    provider.provide(add_movie_contribution_collection_factory)
    provider.provide(edit_movie_contribution_collection_factory)
    provider.provide(add_person_contribution_collection_factory)
    provider.provide(edit_person_contribution_collection_factory)
    provider.provide(achievement_collection_factory)

    return provider


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
