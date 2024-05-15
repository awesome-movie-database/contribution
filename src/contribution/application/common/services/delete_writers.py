from typing import Sequence

from contribution.domain import WriterId
from contribution.application.common.exceptions import WritersDoNotExistError
from contribution.application.common.gateways import WriterGateway


class DeleteWriters:
    def __init__(self, writer_gateway: WriterGateway):
        self._writer_gateway = writer_gateway

    async def __call__(self, writers_ids: Sequence[WriterId]) -> None:
        await self._ensure_writers_exist(writers_ids)

        writers = await self._writer_gateway.list_with_ids(*writers_ids)
        await self._writer_gateway.delete_seq(writers)

    async def _ensure_writers_exist(
        self,
        writers_ids: Sequence[WriterId],
    ) -> None:
        writers = await self._writer_gateway.list_with_ids(*writers_ids)
        some_of_writers_are_missing = len(writers_ids) != len(writers)

        if some_of_writers_are_missing:
            ids_of_missing_writers = set(writers_ids).difference(
                [writer.id for writer in writers],
            )
            raise WritersDoNotExistError(list(ids_of_missing_writers))
