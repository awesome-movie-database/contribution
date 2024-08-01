# Fuck pydantic
# mypy: disable-error-code="assignment"

from typing import Optional
from datetime import date

from pydantic import BaseModel

from contribution.domain import (
    Sex,
    PersonId,
    PhotoUrl,
    Maybe,
)
from contribution.application.commands import EditPersonCommand


class EditPersonRequest(BaseModel):
    person_id: PersonId
    first_name: str = None
    last_name: str = None
    sex: Sex = None
    birth_date: date = None
    death_date: Optional[date] = None
    photos_to_add: list[PhotoUrl]

    def to_command(self) -> EditPersonCommand:
        request_as_dict = self.model_dump(exclude_unset=True)

        first_name = Maybe[str].from_mapping_by_key(
            mapping=request_as_dict,
            key="first_name",
        )
        last_name = Maybe[str].from_mapping_by_key(
            mapping=request_as_dict,
            key="last_name",
        )
        sex = Maybe[Sex].from_mapping_by_key(
            mapping=request_as_dict,
            key="sex",
        )
        birth_date = Maybe[date].from_mapping_by_key(
            mapping=request_as_dict,
            key="birth_date",
        )
        death_date = Maybe[Optional[date]].from_mapping_by_key(
            mapping=request_as_dict,
            key="death_date",
        )

        return EditPersonCommand(
            person_id=self.person_id,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birth_date=birth_date,
            death_date=death_date,
            photos_to_add=self.photos_to_add,
        )
