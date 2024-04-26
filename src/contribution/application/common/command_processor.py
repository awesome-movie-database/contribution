from typing import TypeVar, Protocol


_C = TypeVar("_C", contravariant=True)
_R = TypeVar("_R", covariant=True)


class CommandProcessor(Protocol[_C, _R]):
    async def process(self, command: _C) -> _R:
        raise NotImplementedError
