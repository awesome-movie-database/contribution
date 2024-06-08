from dataclasses import dataclass

from contribution.domain import PersonId
from contribution.application import OperationId


@dataclass(frozen=True, slots=True)
class IncomingPersonUpdatedEvent:
    operation_id: OperationId
    person_id: PersonId
