from typing import Optional
from datetime import date, datetime

from contribution.domain.constants import ContributionStatus
from contribution.domain.value_objects import AddPersonContributionId
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
        validate_person_first_name: ValidatePersonFirstName,
        validate_person_last_name: ValidatePersonLastName,
    ):
        self._validate_person_first_name = validate_person_first_name
        self._validate_person_last_name = validate_person_last_name

    def __call__(
        self,
        *,
        id: AddPersonContributionId,
        author: User,
        first_name: str,
        last_name: str,
        birth_date: date,
        death_date: Optional[date],
        current_timestamp: datetime,
    ) -> AddPersonContribution:
        if not author.is_active:
            raise UserIsNotActiveError()

        self._validate_person_first_name(first_name)
        self._validate_person_last_name(last_name)

        if death_date and death_date < birth_date:
            raise InvalidPersonBirthOrDeathDateError()

        return AddPersonContribution(
            id=id,
            author_id=author.id,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            death_date=death_date,
            status=ContributionStatus.PENDING,
            created_at=current_timestamp,
            updated_at=None,
        )
