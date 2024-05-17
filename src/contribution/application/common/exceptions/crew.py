from typing import Collection

from contribution.domain import CrewMemberId
from .base import ApplicationError


class CrewMembersAlreadyExistError(ApplicationError):
    def __init__(
        self,
        ids_of_existing_crew_members: Collection[CrewMemberId],
    ):
        self.ids_of_existing_crew_members = ids_of_existing_crew_members


class CrewMembersDoNotExistError(ApplicationError):
    def __init__(
        self,
        ids_of_missing_crew_members: Collection[CrewMemberId],
    ):
        self.ids_of_missing_crew_members = ids_of_missing_crew_members
