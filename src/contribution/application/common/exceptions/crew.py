from typing import Collection

from contribution.domain import CrewMemberId
from .base import ApplicationError


class CrewMembersAlreadyExistError(ApplicationError):
    def __init__(self, crew_member_ids: Collection[CrewMemberId]):
        self.crew_member_ids = crew_member_ids


class CrewMembersDoNotExistError(ApplicationError):
    def __init__(self, crew_member_ids: Collection[CrewMemberId]):
        self.crew_member_ids = crew_member_ids
