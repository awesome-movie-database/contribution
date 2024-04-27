class AccessConcern:
    def authorize(
        self,
        current_user_permissions: int,
        required_permissions: int,
    ) -> bool:
        return (
            current_user_permissions & required_permissions
            == required_permissions
        )
