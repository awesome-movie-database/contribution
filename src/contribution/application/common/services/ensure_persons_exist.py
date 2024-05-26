from typing import Collection

from contribution.domain import PersonId
from contribution.application.common.exceptions import PersonsDoNotExistError
from contribution.application.common.gateways import PersonGateway


class EnsurePersonsExist:
    def __init__(self, person_gateway: PersonGateway):
        self._person_gateway = person_gateway

    async def __call__(self, person_ids: Collection[PersonId]) -> None:
        persons = await self._person_gateway.list_by_ids(person_ids)
        some_persons_are_missing = len(persons) != len(person_ids)

        if some_persons_are_missing:
            ids_of_persons_from_gateway = [person for person in persons]
            ids_of_missing_persons = set(person_ids).difference(
                ids_of_persons_from_gateway,
            )
            raise PersonsDoNotExistError(list(ids_of_missing_persons))
