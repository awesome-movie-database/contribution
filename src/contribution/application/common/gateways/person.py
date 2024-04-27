from typing import Protocol, Optional

from contribution.domain.value_objects import PersonId
from contribution.domain.entities import Person


class PersonGateway(Protocol):
    async def with_id(self, id: PersonId) -> Optional[Person]:
        raise NotImplementedError

    async def acquire_with_id(self, id: PersonId) -> Optional[Person]:
        raise NotImplementedError

    async def list_with_ids(self, *ids: PersonId) -> list[Person]:
        raise NotImplementedError

    async def save(self, person: Person) -> None:
        raise NotImplementedError

    async def update(self, person: Person) -> None:
        raise NotImplementedError
