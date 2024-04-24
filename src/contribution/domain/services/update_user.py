from contribution.domain.entities import User
from contribution.domain.maybe import Maybe


class UpdateUser:
    def __call__(
        self,
        user: User,
        *,
        name: Maybe[str],
        is_active: Maybe[bool],
    ) -> None:
        if name.is_set:
            user.name = name.value
        if is_active.is_set:
            user.is_active = is_active.value
