from dataclasses import dataclass

from contribution.domain import PersonId
from contribution.application import CorrelationId


@dataclass(frozen=True, slots=True)
class IncomingPersonCreatedEvent:
    correlation_id: CorrelationId
    person_id: PersonId
