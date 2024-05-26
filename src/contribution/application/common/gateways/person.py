from typing import Iterable, Protocol, Optional

from contribution.domain import PersonId, Person


class PersonGateway(Protocol):
    async def by_id(self, id: PersonId) -> Optional[Person]:
        raise NotImplementedError

    async def acquire_by_id(self, id: PersonId) -> Optional[Person]:
        raise NotImplementedError

    async def list_by_ids(
        self,
        ids: Iterable[PersonId],
    ) -> list[Person]:
        raise NotImplementedError

    async def save(self, person: Person) -> None:
        raise NotImplementedError

    async def update(self, person: Person) -> None:
        raise NotImplementedError
