from dataclasses import dataclass

from contribution.domain import UserId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class IncomingUserCreatedEvent:
    operation_id: OperationId
    user_id: UserId
