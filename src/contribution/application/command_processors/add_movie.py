from datetime import datetime, timezone
from typing import Sequence

from uuid_extensions import uuid7

from contribution.domain.value_objects import (
    PersonId,
    AddMovieContributionId,
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
)
from contribution.domain.entities import Person
from contribution.domain.services import AddMovie
from contribution.application.common.services import AccessConcern
from contribution.application.common.command_processor import (
    CommandProcessor,
)
from contribution.application.common.transaction_processor import (
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    UserDoesNotExistError,
    PersonsDoNotExistError,
    NotEnoughPermissionsError,
)
from contribution.application.common.gateways import (
    AddMovieContributionGateway,
    UserGateway,
    PersonGateway,
    PermissionsGateway,
)
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.common.identity_provider import IdentityProvider
from contribution.application.commands import AddMovieCommand


def add_movie_factory(
    add_movie: AddMovie,
    access_concern: AccessConcern,
    add_movie_contribution_gateway: AddMovieContributionGateway,
    user_gateway: UserGateway,
    person_gateway: PersonGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    identity_provider: IdentityProvider,
) -> CommandProcessor[AddMovieCommand, AddMovieContributionId]:
    add_movie_processor = AddMovieProcessor(
        add_movie=add_movie,
        add_movie_contribution_gateway=add_movie_contribution_gateway,
        user_gateway=user_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
    )
    authz_processor = AuthorizationProcessor(
        processor=add_movie_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    tx_processor = TransactionProcessor(
        processor=authz_processor,
        unit_of_work=unit_of_work,
    )
    return tx_processor


class AddMovieProcessor:
    def __init__(
        self,
        *,
        add_movie: AddMovie,
        add_movie_contribution_gateway: AddMovieContributionGateway,
        user_gateway: UserGateway,
        person_gateway: PersonGateway,
        identity_provider: IdentityProvider,
    ):
        self._add_movie = add_movie
        self._add_movie_contribution_gateway = add_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._person_gateway = person_gateway
        self._identity_provider = identity_provider

    async def process(
        self,
        command: AddMovieCommand,
    ) -> AddMovieContributionId:
        current_user_id = await self._identity_provider.user_id()

        author = await self._user_gateway.with_id(current_user_id)
        if not author:
            raise UserDoesNotExistError(current_user_id)

        await self._ensure_persons_exist(
            roles=command.roles,
            writers=command.writers,
            crew=command.crew,
        )

        contribution = self._add_movie(
            id=AddMovieContributionId(uuid7()),
            author=author,
            title=command.title,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
            roles=command.roles,
            writers=command.writers,
            crew=command.crew,
            current_timestamp=datetime.now(timezone.utc),
        )
        await self._add_movie_contribution_gateway.save(contribution)

        return contribution.id

    async def _ensure_persons_exist(
        self,
        *,
        roles: Sequence[ContributionRole],
        writers: Sequence[ContributionWriter],
        crew: Sequence[ContributionCrewMember],
    ) -> None:
        persons_ids = []

        for role in roles:
            persons_ids.append(role.person_id)
        for writer in writers:
            persons_ids.append(writer.person_id)
        for crew_member in crew:
            persons_ids.append(crew_member.person_id)

        persons = await self._person_gateway.list_with_ids(*persons_ids)
        some_of_persons_do_not_exist = len(persons_ids) != len(persons)

        if some_of_persons_do_not_exist:
            self._some_persons_do_not_exist_handler(
                persons_ids=persons_ids,
                persons_from_gateway=persons,
            )

    def _some_persons_do_not_exist_handler(
        self,
        *,
        persons_ids: Sequence[PersonId],
        persons_from_gateway: Sequence[Person],
    ) -> None:
        ids_of_persons_from_gateway = [
            person_from_gateway.id
            for person_from_gateway in persons_from_gateway
        ]
        ids_of_missing_persons = set(persons_ids).difference(
            ids_of_persons_from_gateway,
        )
        raise PersonsDoNotExistError(list(ids_of_missing_persons))


class AuthorizationProcessor:
    def __init__(
        self,
        *,
        processor: AddMovieProcessor,
        access_concern: AccessConcern,
        permissions_gateway: PermissionsGateway,
        identity_provider: IdentityProvider,
    ):
        self._processor = processor
        self._access_concern = access_concern
        self._permissions_gateway = permissions_gateway
        self._identity_provider = identity_provider

    async def process(
        self,
        command: AddMovieCommand,
    ) -> AddMovieContributionId:
        current_user_permissions = await self._identity_provider.permissions()
        required_permissions = (
            await self._permissions_gateway.for_contribution()
        )

        access = self._access_concern.authorize(
            current_user_permissions,
            required_permissions,
        )
        if not access:
            raise NotEnoughPermissionsError()

        return await self._processor.process(command)
