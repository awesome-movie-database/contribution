from contribution.domain.value_objects import WriterId
from contribution.application.common.exceptions import WritersAlreadyExistError
from contribution.application.common.gateways import WriterGateway


class EnsureWritersDoNotExist:
    def __init__(self, writer_gateway: WriterGateway):
        self._writer_gateway = writer_gateway

    async def __call__(self, *writers_ids: WriterId) -> None:
        writers_from_gateway = await self._writer_gateway.list_with_ids(
            *writers_ids,
        )
        if writers_from_gateway:
            ids_of_writers_from_gateway = [
                writer_from_gateway.id
                for writer_from_gateway in writers_from_gateway
            ]
            raise WritersAlreadyExistError(
                ids_of_existing_writers=ids_of_writers_from_gateway,
            )
