from contribution.domain.validators import ValidateUserName
from contribution.domain.entities import User
from contribution.domain.maybe import Maybe


class UpdateUser:
    def __init__(
        self,
        validate_user_name: ValidateUserName,
    ):
        self._validate_user_name = validate_user_name

    def __call__(
        self,
        user: User,
        *,
        name: Maybe[str],
        is_active: Maybe[bool],
    ) -> None:
        if name.is_set:
            self._validate_user_name(name.value)
            user.name = name.value
        if is_active.is_set:
            user.is_active = is_active.value
