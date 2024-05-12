from typing import Protocol


class CommandProcessor[C, R](Protocol):
    async def process(self, command: C) -> R:
        raise NotImplementedError
