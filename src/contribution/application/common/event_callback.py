from typing import Protocol


class OnEventOccurred[E](Protocol):
    async def __call__(self, event: E) -> None:
        raise NotImplementedError
