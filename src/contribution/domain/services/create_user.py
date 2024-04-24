from contribution.domain.value_objects import UserId
from contribution.domain.entities import User


class CreateUser:
    def __call__(
        self,
        *,
        id: UserId,
        name: str,
        is_active: bool,
    ) -> User:
        return User(
            id=id,
            name=name,
            is_active=is_active,
            rating=0,
            contributions_count=0,
        )
