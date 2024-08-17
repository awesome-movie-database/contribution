import logging
from datetime import datetime, timezone

from uuid_extensions import uuid7

from contribution.domain import (
    AddMovieContributionId,
    UserIsNotActiveError,
    AddMovie,
)
from contribution.application.common import (
    OperationId,
    AccessConcern,
    EnsurePersonsExist,
    CreateMovieRoles,
    CreateMovieWriters,
    CreateMovieCrew,
    CommandProcessor,
    AuthorizationProcessor,
    TransactionProcessor,
    UserDoesNotExistError,
    PersonsDoNotExistError,
    NotEnoughPermissionsError,
    AddMovieContributionGateway,
    UserGateway,
    PermissionsGateway,
    UnitOfWork,
    IdentityProvider,
    OnEventOccurred,
    MovieAddedEvent,
    make_func_cacheable,
)
from contribution.application.commands import AddMovieCommand


logger = logging.getLogger(__name__)


def add_movie_factory(
    operation_id: OperationId,
    add_movie: AddMovie,
    access_concern: AccessConcern,
    ensure_persons_exist: EnsurePersonsExist,
    create_movie_roles: CreateMovieRoles,
    create_movie_writers: CreateMovieWriters,
    create_movie_crew: CreateMovieCrew,
    add_movie_contribution_gateway: AddMovieContributionGateway,
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    identity_provider: IdentityProvider,
    on_movie_added: OnEventOccurred[MovieAddedEvent],
) -> CommandProcessor[AddMovieCommand, AddMovieContributionId]:
    current_timestamp = datetime.now(timezone.utc)

    create_movie_roles = make_func_cacheable(create_movie_roles)
    create_movie_writers = make_func_cacheable(create_movie_writers)
    create_movie_crew = make_func_cacheable(create_movie_crew)

    add_movie_processor = AddMovieProcessor(
        add_movie=add_movie,
        ensure_persons_exist=ensure_persons_exist,
        create_movie_roles=create_movie_roles,
        create_movie_writers=create_movie_writers,
        create_movie_crew=create_movie_crew,
        add_movie_contribution_gateway=add_movie_contribution_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        current_timestamp=current_timestamp,
    )
    authz_processor = AuthorizationProcessor(
        processor=add_movie_processor,
        access_concern=access_concern,
        permissions_gateway=permissions_gateway,
        identity_provider=identity_provider,
    )
    callback_processor = AddMovieCallbackProcessor(
        processor=authz_processor,
        create_movie_roles=create_movie_roles,
        create_movie_writers=create_movie_writers,
        create_movie_crew=create_movie_crew,
        identity_provider=identity_provider,
        on_movie_added=on_movie_added,
        current_timestamp=current_timestamp,
    )
    tx_processor = TransactionProcessor(
        processor=callback_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = AddMovieLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
        identity_provider=identity_provider,
    )

    return log_processor


class AddMovieProcessor:
    def __init__(
        self,
        *,
        add_movie: AddMovie,
        ensure_persons_exist: EnsurePersonsExist,
        create_movie_roles: CreateMovieRoles,
        create_movie_writers: CreateMovieWriters,
        create_movie_crew: CreateMovieCrew,
        add_movie_contribution_gateway: AddMovieContributionGateway,
        user_gateway: UserGateway,
        identity_provider: IdentityProvider,
        current_timestamp: datetime,
    ):
        self._add_movie = add_movie
        self._ensure_persons_exist = ensure_persons_exist
        self._create_movie_roles = create_movie_roles
        self._create_movie_writers = create_movie_writers
        self._create_movie_crew = create_movie_crew
        self._add_movie_contribution_gateway = add_movie_contribution_gateway
        self._user_gateway = user_gateway
        self._identity_provider = identity_provider
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: AddMovieCommand,
    ) -> AddMovieContributionId:
        current_user_id = await self._identity_provider.user_id()

        author = await self._user_gateway.by_id(current_user_id)
        if not author:
            raise UserDoesNotExistError()

        person_ids = [
            *(role.person_id for role in command.roles),
            *(writer.person_id for writer in command.writers),
            *(crew_member.person_id for crew_member in command.crew),
        ]
        await self._ensure_persons_exist(person_ids)

        movie_roles = self._create_movie_roles(command.roles)
        movie_writers = self._create_movie_writers(command.writers)
        movie_crew = self._create_movie_crew(command.crew)

        contribution = self._add_movie(
            id=AddMovieContributionId(uuid7()),
            author=author,
            eng_title=command.eng_title,
            original_title=command.original_title,
            summary=command.summary,
            description=command.description,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
            roles=movie_roles,
            writers=movie_writers,
            crew=movie_crew,
            photos=command.photos,
            current_timestamp=self._current_timestamp,
        )
        await self._add_movie_contribution_gateway.save(contribution)

        return contribution.id


class AddMovieCallbackProcessor:
    def __init__(
        self,
        *,
        processor: AuthorizationProcessor,
        create_movie_roles: CreateMovieRoles,
        create_movie_writers: CreateMovieWriters,
        create_movie_crew: CreateMovieCrew,
        identity_provider: IdentityProvider,
        on_movie_added: OnEventOccurred[MovieAddedEvent],
        current_timestamp: datetime,
    ):
        self._processor = processor
        self._create_movie_roles = create_movie_roles
        self._create_movie_writers = create_movie_writers
        self._create_movie_crew = create_movie_crew
        self._identity_provider = identity_provider
        self._on_movie_added = on_movie_added
        self._current_timestamp = current_timestamp

    async def process(
        self,
        command: AddMovieCommand,
    ) -> AddMovieContributionId:
        result = await self._processor.process(command)
        current_user_id = await self._identity_provider.user_id()

        movie_roles = self._create_movie_roles(command.roles)
        movie_writers = self._create_movie_writers(command.writers)
        movie_crew = self._create_movie_crew(command.crew)

        event = MovieAddedEvent(
            contribution_id=result,
            author_id=current_user_id,
            eng_title=command.eng_title,
            original_title=command.original_title,
            summary=command.summary,
            description=command.description,
            release_date=command.release_date,
            countries=command.countries,
            genres=command.genres,
            mpaa=command.mpaa,
            duration=command.duration,
            budget=command.budget,
            revenue=command.revenue,
            roles=movie_roles,
            writers=movie_writers,
            crew=movie_crew,
            photos=command.photos,
            added_at=self._current_timestamp,
        )
        await self._on_movie_added(event)

        return result


class AddMovieLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
        identity_provider: IdentityProvider,
    ):
        self._processor = processor
        self._operation_id = operation_id
        self._identity_provider = identity_provider

    async def process(
        self,
        command: AddMovieCommand,
    ) -> AddMovieContributionId:
        current_user_id = await self._identity_provider.user_id()

        logger.debug(
            "'Add Movie' command processing started",
            extra={
                "operation_id": self._operation_id,
                "user_id": current_user_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except NotEnoughPermissionsError as error:
            logger.info(
                "Expected error occurred: User has not enough permissions",
                extra={
                    "operation_id": self._operation_id,
                    "current_user_permissions": (
                        await self._identity_provider.permissions()
                    ),
                },
            )
            raise error
        except UserDoesNotExistError as error:
            logger.error(
                "Unexpected error occurred: "
                "User is authenticated, but user gateway returns None",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except UserIsNotActiveError as error:
            logger.info(
                "Expected error occurred: User is not active",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except PersonsDoNotExistError as error:
            logger.info(
                "Expected error occurred: "
                "Person ids entered by user do not belong to any persons",
                extra={
                    "operation_id": self._operation_id,
                    "non_existing_person_ids": error.person_ids,
                },
            )
            raise error
        except Exception as error:
            logger.exception(
                "Unexpected error occurred",
                extra={"operation_id": self._operation_id},
            )
            raise error

        logger.debug(
            "'Add Movie' command processing completed",
            extra={
                "operation_id": self._operation_id,
                "contribution_id": result,
            },
        )

        return result
