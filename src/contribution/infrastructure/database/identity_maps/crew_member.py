from typing import Optional

from contribution.domain import CrewMemberId, CrewMember


class CrewMemberMap:
    def __init__(self):
        self._crew_members: list[CrewMember] = list()

    def by_id(self, id: CrewMemberId) -> Optional[CrewMember]:
        for crew_member in self._crew_members:
            if crew_member.id == id:
                return crew_member
        return None

    def save(self, crew_member: CrewMember) -> None:
        """
        Saves crew member in identity map if crew member doesn't
        exist, otherwise raises ValueError.
        """
        crew_member_from_map = self.by_id(crew_member.id)
        if crew_member_from_map:
            message = "Crew member already exists in identity map"
            raise ValueError(message)
        self._crew_members.append(crew_member)
