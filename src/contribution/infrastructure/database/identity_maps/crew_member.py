from typing import Optional

from contribution.domain import CrewMemberId, CrewMember


class CrewMemberMap:
    def __init__(self):
        self._crew_members: set[CrewMember] = set()

    def with_id(self, id: CrewMemberId) -> Optional[CrewMember]:
        for crew_member in self._crew_members:
            if crew_member.id == id:
                return crew_member
        return None

    def save(self, crew_member: CrewMember) -> None:
        """
        Saves crew member in identity map if crew member doesn't
        exist, otherwise raises ValueError.
        """
        crew_member_from_map = self.with_id(crew_member.id)
        if crew_member_from_map:
            message = "Crew member already exists in identity map"
            raise ValueError(message)
        self._crew_members.add(crew_member)

    def update(self, crew_member: CrewMember) -> None:
        """
        Updates crew member in identity map if crew member exists,
        otherwise raises ValueError.
        """
        crew_member_from_map = self.with_id(crew_member.id)
        if not crew_member_from_map:
            message = "Crew member doesn't exist in identity map"
            raise ValueError(message)
        self._crew_members.remove(crew_member_from_map)
        self._crew_members.add(crew_member)
