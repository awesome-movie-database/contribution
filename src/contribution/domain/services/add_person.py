from typing import Iterable, Optional
from datetime import date, datetime

from contribution.domain.constants import (
    ContributionStatus,
    Sex,
)
from contribution.domain.value_objects import (
    AddPersonContributionId,
    PhotoUrl,
)
from contribution.domain.validators import (
    ValidatePersonFirstName,
    ValidatePersonLastName,
)
from contribution.domain.exceptions import (
    UserIsNotActiveError,
    InvalidPersonBirthOrDeathDateError,
)
from contribution.domain.entities import (
    AddPersonContribution,
    User,
)


class AddPerson:
    def __init__(
        self,
        validate_first_name: ValidatePersonFirstName,
        validate_last_name: ValidatePersonLastName,
    ):
        self._validate_first_name = validate_first_name
        self._validate_last_name = validate_last_name

    def __call__(
        self,
        *,
        id: AddPersonContributionId,
        author: User,
        first_name: str,
        last_name: str,
        sex: Sex,
        birth_date: date,
        death_date: Optional[date],
        photos: Iterable[PhotoUrl],
        current_timestamp: datetime,
    ) -> AddPersonContribution:
        if not author.is_active:
            raise UserIsNotActiveError()

        self._validate_first_name(first_name)
        self._validate_last_name(last_name)

        if death_date and death_date < birth_date:
            raise InvalidPersonBirthOrDeathDateError()

        return AddPersonContribution(
            id=id,
            author_id=author.id,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birth_date=birth_date,
            death_date=death_date,
            photos=photos,
            status=ContributionStatus.PENDING,
            created_at=current_timestamp,
            status_updated_at=None,
        )
