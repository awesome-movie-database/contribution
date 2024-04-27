from typing import Generic, TypeVar

from contribution.application.common.unit_of_work import UnitOfWork
from .command_processor import CommandProcessor


_C = TypeVar("_C", contravariant=True)
_R = TypeVar("_R", covariant=True)


class TransactionProcessor(Generic[_C, _R]):
    def __init__(
        self,
        *,
        processor: CommandProcessor[_C, _R],
        unit_of_work: UnitOfWork,
    ):
        self._processor = processor
        self._unit_of_work = unit_of_work

    async def process(self, command: _C) -> _R:
        result = await self._processor.process(command)
        await self._unit_of_work.commit()
        return result
