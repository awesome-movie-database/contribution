from typing import Collection

from contribution.domain import WriterId
from contribution.application.common.exceptions import WritersDoNotExistError
from contribution.application.common.gateways import WriterGateway


class DeleteWriters:
    def __init__(self, writer_gateway: WriterGateway):
        self._writer_gateway = writer_gateway

    async def __call__(self, writer_ids: Collection[WriterId]) -> None:
        await self._ensure_writers_exist(writer_ids)

        writers = await self._writer_gateway.list_by_ids(writer_ids)
        await self._writer_gateway.delete_many(writers)

    async def _ensure_writers_exist(
        self,
        writer_ids: Collection[WriterId],
    ) -> None:
        writers = await self._writer_gateway.list_by_ids(writer_ids)

        some_of_writers_are_missing = len(writer_ids) != len(writers)
        if some_of_writers_are_missing:
            ids_of_writers_from_gateway = [writer.id for writer in writers]
            non_existing_writer_ids = set(writer_ids).difference(
                ids_of_writers_from_gateway,
            )
            raise WritersDoNotExistError(non_existing_writer_ids)
