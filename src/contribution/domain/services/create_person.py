from typing import Optional
from datetime import date

from contribution.domain.constants import Sex
from contribution.domain.value_objects import PersonId
from contribution.domain.validators import (
    ValidatePersonFirstName,
    ValidatePersonLastName,
)
from contribution.domain.exceptions import (
    InvalidPersonBirthOrDeathDateError,
)
from contribution.domain.entities import Person


class CreatePerson:
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
        id: PersonId,
        first_name: str,
        last_name: str,
        sex: Sex,
        birth_date: date,
        death_date: Optional[date],
    ) -> Person:
        self._validate_first_name(first_name)
        self._validate_last_name(last_name)

        if death_date and death_date < birth_date:
            raise InvalidPersonBirthOrDeathDateError()

        return Person(
            id=id,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birth_date=birth_date,
            death_date=death_date,
        )
