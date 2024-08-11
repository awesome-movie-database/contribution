from datetime import date, datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest
from uuid_extensions import uuid7

from contribution.domain import (
    Genre,
    MPAA,
    Money,
    UserId,
    User,
    ValidateMovieEngTitle,
    ValidateMovieOriginalTitle,
    ValidateMovieDuration,
    ValidateRoleCharacter,
    ValidateRoleImportance,
    AddMovie,
)
from contribution.application import (
    EnsurePersonsExist,
    CreateMovieRoles,
    CreateMovieWriters,
    CreateMovieCrew,
    TransactionProcessor,
    AddMovieContributionGateway,
    UserGateway,
    UnitOfWork,
    AddMovieCommand,
    AddMovieProcessor,
)


@pytest.mark.usefixtures("clear_database")
async def test_add_movie(
    ensure_persons_exist: EnsurePersonsExist,
    add_movie_contribution_gateway: AddMovieContributionGateway,
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
):
    current_timestamp = datetime.now(timezone.utc)

    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email=None,
        telegram=None,
        is_active=True,
        rating=0,
        accepted_contributions_count=0,
        rejected_contributions_count=0,
    )
    await user_gateway.save(user)

    identity_provider = AsyncMock()
    identity_provider.user_id = AsyncMock(return_value=user.id)

    command = AddMovieCommand(
        eng_title="Matrix",
        original_title="Matrix",
        release_date=date(1999, 3, 31),
        countries=["US"],
        genres=[Genre.ACTION, Genre.FANTASY, Genre.SCI_FI],
        mpaa=MPAA.R,
        duration=134,
        budget=Money(amount=Decimal("63000000"), currency="USD"),
        revenue=Money(amount=Decimal("467826932"), currency="USD"),
        roles=[],
        writers=[],
        crew=[],
        photos=[],
    )
    add_movie = AddMovie(
        validate_eng_title=ValidateMovieEngTitle(),
        validate_original_title=ValidateMovieOriginalTitle(),
        valudate_duration=ValidateMovieDuration(),
    )
    create_movie_roles = CreateMovieRoles(
        validate_role_character=ValidateRoleCharacter(),
        validate_role_importance=ValidateRoleImportance(),
    )
    add_movie_processor = AddMovieProcessor(
        add_movie=add_movie,
        ensure_persons_exist=ensure_persons_exist,
        create_movie_roles=create_movie_roles,
        create_movie_writers=CreateMovieWriters(),
        create_movie_crew=CreateMovieCrew(),
        add_movie_contribution_gateway=add_movie_contribution_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        current_timestamp=current_timestamp,
    )
    tx_processor = TransactionProcessor(
        processor=add_movie_processor,
        unit_of_work=unit_of_work,
    )

    await tx_processor.process(command)
