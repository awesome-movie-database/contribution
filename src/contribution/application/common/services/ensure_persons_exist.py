from contribution.domain.value_objects import PersonId
from contribution.application.common.exceptions import PersonsDoNotExistError
from contribution.application.common.gateways import PersonGateway


class EnsurePersonsExist:
    def __init__(self, person_gateway: PersonGateway):
        self._person_gateway = person_gateway

    async def __call__(self, *persons_ids: PersonId) -> None:
        persons_from_gateway = await self._person_gateway.list_with_ids(
            *persons_ids,
        )
        some_of_persons_do_not_exist = len(persons_ids) != len(
            persons_from_gateway,
        )

        if some_of_persons_do_not_exist:
            ids_of_persons_from_gateway = [
                person_from_gateway.id
                for person_from_gateway in persons_from_gateway
            ]
            ids_of_missing_persons = set(persons_ids).difference(
                ids_of_persons_from_gateway,
            )
            raise PersonsDoNotExistError(list(ids_of_missing_persons))
