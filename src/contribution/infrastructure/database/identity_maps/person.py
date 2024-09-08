from dataclasses import dataclass
from typing import Optional

from contribution.domain import PersonId, Person


@dataclass(slots=True)
class PersonMapUnit:
    person: Person
    is_acquired: bool


class PersonMap:
    def __init__(self):
        self._units: list[PersonMapUnit] = list()

    def by_id(self, id: PersonId) -> Optional[Person]:
        for unit in self._units:
            if unit.person.id == id:
                return unit.person
        return None

    def save(self, person: Person) -> None:
        """
        Saves person in identity map if person doesn't
        exist, otherwise raises Exception.
        """
        person_from_map = self.by_id(person.id)
        if person_from_map:
            message = "Person already exists in identity map"
            raise Exception(message)
        unit = PersonMapUnit(person=person, is_acquired=False)
        self._units.append(unit)

    def save_acquired(self, person: Person) -> None:
        """
        Saves person as acquired in identity map if person
        doesn't exist or already exist and not marked as
        acquired, otherwise raises Exception.
        """
        person_from_map = self.by_id(person.id)
        if not person_from_map:
            unit = PersonMapUnit(person=person, is_acquired=True)
            self._units.append(unit)
            return

        person_is_acquired = self.is_acquired(person)
        if person_is_acquired:
            message = (
                "Person already exists in identity map and"
                "marked as acquired"
            )
            raise Exception(message)

        for unit in self._units:
            if unit.person == person:
                unit.is_acquired = True
                return

    def is_acquired(self, person: Person) -> bool:
        """
        Returns whether person is acquired if person exists
        in identity map, otherwise raises Exception.
        """
        for unit in self._units:
            if unit.person == person:
                return unit.is_acquired
        message = "Person doesn't exist in identity map"
        raise Exception(message)
