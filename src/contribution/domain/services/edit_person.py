from typing import Iterable, Optional
from datetime import date, datetime

from contribution.domain.constants import (
    ContributionStatus,
    Sex,
)
from contribution.domain.value_objects import EditPersonContributionId
from contribution.domain.validators import (
    ValidatePersonFirstName,
    ValidatePersonLastName,
)
from contribution.domain.exceptions import (
    UserIsNotActiveError,
    InvalidPersonBirthOrDeathDateError,
    ContributionDataDuplicationError,
)
from contribution.domain.models import (
    PhotoUrl,
    EditPersonContribution,
    User,
    Person,
)
from contribution.domain.maybe import Maybe


class EditPerson:
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
        id: EditPersonContributionId,
        author: User,
        person: Person,
        first_name: Maybe[str],
        last_name: Maybe[str],
        sex: Maybe[Sex],
        birth_date: Maybe[date],
        death_date: Maybe[Optional[date]],
        photos_to_add: Iterable[PhotoUrl],
        current_timestamp: datetime,
    ) -> EditPersonContribution:
        if not author.is_active:
            raise UserIsNotActiveError()

        if first_name.is_set:
            self._validate_first_name(first_name.value)
        if last_name.is_set:
            self._validate_last_name(last_name.value)

        if (
            birth_date.is_set
            and not death_date.is_set
            and person.death_date
            and person.death_date < birth_date.value
        ):
            raise InvalidPersonBirthOrDeathDateError()
        elif (
            death_date.is_set
            and not birth_date.is_set
            and death_date.value
            and death_date.value < person.birth_date
        ):
            raise InvalidPersonBirthOrDeathDateError()
        elif (
            death_date.is_set
            and birth_date.is_set
            and death_date.value
            and death_date.value < birth_date.value
        ):
            raise InvalidPersonBirthOrDeathDateError()

        self._ensure_contribution_does_not_duplicate_person_fields_values(
            person=person,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birth_date=birth_date,
            death_date=death_date,
        )

        return EditPersonContribution(
            id=id,
            author_id=author.id,
            person_id=person.id,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birth_date=birth_date,
            death_date=death_date,
            photos_to_add=photos_to_add,
            status=ContributionStatus.PENDING,
            created_at=current_timestamp,
            status_updated_at=None,
        )

    def _ensure_contribution_does_not_duplicate_person_fields_values(
        self,
        *,
        person: Person,
        first_name: Maybe[str],
        last_name: Maybe[str],
        sex: Maybe[Sex],
        birth_date: Maybe[date],
        death_date: Maybe[Optional[date]],
    ) -> None:
        fields_with_duplicates = []

        if first_name.is_set and first_name.value == person.first_name:
            fields_with_duplicates.append("first_name")
        if last_name.is_set and last_name.value == person.last_name:
            fields_with_duplicates.append("last_name")
        if sex.is_set and sex.value == person.sex:
            fields_with_duplicates.append("sex")
        if birth_date.is_set and birth_date.value == person.birth_date:
            fields_with_duplicates.append("birth_date")
        if death_date.is_set and death_date.value == person.death_date:
            fields_with_duplicates.append("death_date")

        if fields_with_duplicates:
            raise ContributionDataDuplicationError(fields_with_duplicates)
