from typing import Iterable, Protocol, Optional

from contribution.domain import WriterId, Writer


class WriterGateway(Protocol):
    async def with_id(self, id: WriterId) -> Optional[Writer]:
        raise NotImplementedError

    async def list_with_ids(
        self,
        ids: Iterable[WriterId],
    ) -> list[Writer]:
        raise NotImplementedError

    async def save_many(self, writers: Iterable[Writer]) -> None:
        raise NotImplementedError

    async def update(self, writer: Writer) -> None:
        raise NotImplementedError

    async def delete_many(self, writers: Iterable[Writer]) -> None:
        raise NotImplementedError
