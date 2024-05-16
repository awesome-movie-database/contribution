from typing import Optional

from contribution.domain import PersonId, Person


class PersonMap:
    def __init__(self):
        self._persons: set[Person] = set()

    def with_id(self, id: PersonId) -> Optional[Person]:
        for person in self._persons:
            if person.id == id:
                return person
        return None

    def save(self, person: Person) -> None:
        """
        Saves person in identity map if person doesn't
        exist, otherwise raises ValueError.
        """
        person_from_map = self.with_id(person.id)
        if person_from_map:
            message = "Person already exists in identity map"
            raise ValueError(message)
        self._persons.add(person)

    def update(self, person: Person) -> None:
        """
        Updates person in identity map if person exists,
        otherwise raises ValueError.
        """
        person_from_map = self.with_id(person.id)
        if not person_from_map:
            message = "Person doesn't exist in identity map"
            raise ValueError(message)
        self._persons.remove(person_from_map)
        self._persons.add(person)
