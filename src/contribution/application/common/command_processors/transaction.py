from contribution.application.common.unit_of_work import UnitOfWork
from .command import CommandProcessor


class TransactionProcessor[C, R]:
    def __init__(
        self,
        *,
        processor: CommandProcessor[C, R],
        unit_of_work: UnitOfWork,
    ):
        self._processor = processor
        self._unit_of_work = unit_of_work

    async def process(self, command: C) -> R:
        result = await self._processor.process(command)
        await self._unit_of_work.commit()
        return result
