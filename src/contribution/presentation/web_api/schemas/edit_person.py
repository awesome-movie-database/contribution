from typing_extensions import Optional, TypedDict, Required
from datetime import date

from contribution.domain.constants import Sex
from contribution.domain.value_objects import PersonId


class EditPersonSchema(TypedDict, total=False):
    person_id: Required[PersonId]
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
