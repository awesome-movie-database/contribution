from typing import Protocol


class PermissionsGateway(Protocol):
    async def for_contribution(self) -> int:
        raise NotImplementedError
