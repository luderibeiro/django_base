class User:
    def __init__(
        self,
        email: str,
        first_name: str,
        last_name: str,
        is_active: bool = True,
        is_staff: bool = False,
        is_superuser: bool = False,
        id: str = None,
    ):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_staff = is_staff
        self.is_superuser = is_superuser

    @property
    def is_admin(self) -> bool:
        return self.is_superuser
