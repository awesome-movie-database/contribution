from dataclasses import dataclass

from contribution.domain import UserId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingUserCreatedEvent:
    correlation_id: CorrelationId
    user_id: UserId
