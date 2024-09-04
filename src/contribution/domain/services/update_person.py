from typing import Optional
from datetime import date

from contribution.domain.constants import Sex
from contribution.domain.validators import (
    ValidatePersonFirstName,
    ValidatePersonLastName,
)
from contribution.domain.exceptions import (
    InvalidPersonBirthOrDeathDateError,
)
from contribution.domain.models import Person
from contribution.domain.maybe import Maybe


class UpdatePerson:
    def __init__(
        self,
        validate_first_name: ValidatePersonFirstName,
        validate_last_name: ValidatePersonLastName,
    ):
        self._validate_first_name = validate_first_name
        self._validate_last_name = validate_last_name

    def __call__(
        self,
        person: Person,
        *,
        first_name: Maybe[str],
        last_name: Maybe[str],
        sex: Maybe[Sex],
        birth_date: Maybe[date],
        death_date: Maybe[Optional[date]],
    ) -> None:
        if first_name.is_set:
            self._validate_first_name(first_name.value)
            person.first_name = first_name.value
        if last_name.is_set:
            self._validate_last_name(last_name.value)
            person.last_name = last_name.value

        if sex.is_set:
            person.sex = sex.value

        if birth_date.is_set and death_date.is_set and death_date.value:
            self._validate_birth_and_death_dates(
                birth_date=birth_date.value,
                death_date=death_date.value,
            )
            person.birth_date = birth_date.value
            person.death_date = death_date.value
        elif not birth_date.is_set and death_date.is_set and death_date.value:
            self._validate_birth_and_death_dates(
                birth_date=person.birth_date,
                death_date=death_date.value,
            )
            person.death_date = death_date.value
        elif birth_date.is_set and not death_date.is_set and person.death_date:
            self._validate_birth_and_death_dates(
                birth_date=birth_date.value,
                death_date=person.death_date,
            )
            person.birth_date = birth_date.value

    def _validate_birth_and_death_dates(
        self,
        birth_date: date,
        death_date: date,
    ) -> None:
        if death_date < birth_date:
            raise InvalidPersonBirthOrDeathDateError()
