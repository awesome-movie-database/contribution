from typing import Protocol, Optional, Sequence

from contribution.domain.value_objects import WriterId
from contribution.domain.entities import Writer


class WriterGateway(Protocol):
    async def with_id(self, id: WriterId) -> Optional[Writer]:
        raise NotImplementedError

    async def list_with_ids(self, *ids: WriterId) -> list[Writer]:
        raise NotImplementedError

    async def save_seq(self, writers: Sequence[Writer]) -> None:
        raise NotImplementedError

    async def update(self, writer: Writer) -> None:
        raise NotImplementedError
