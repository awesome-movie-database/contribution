from typing import TypeVar, Protocol


C = TypeVar("C", contravariant=True)
R = TypeVar("R", covariant=True)


class CommandProcessor(Protocol[C, R]):
    async def process(self, command: C) -> R:
        raise NotImplementedError
