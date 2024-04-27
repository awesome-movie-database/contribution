from typing import Sequence

from contribution.domain.value_objects import CrewMemberId
from .base import ApplicationError


class CrewMembersDoNotExistError(ApplicationError):
    def __init__(
        self,
        ids_of_missing_crew_members: Sequence[CrewMemberId],
    ):
        self.ids_of_missing_crew_members = ids_of_missing_crew_members
