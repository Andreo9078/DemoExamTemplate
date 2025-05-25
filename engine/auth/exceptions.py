from engine.utils import create_handler
from engine.utils import ExceptionRegistry

register = ExceptionRegistry()


@register.exception(create_handler(400))
class UserNotExists(Exception):
    pass


@register.exception(create_handler(400))
class UserAlreadyExists(Exception):
    pass


@register.exception(create_handler(400))
class RoleError(Exception):
    def __init__(self, role_id: int) -> None:
        self.role_id = role_id


@register.exception(create_handler(400))
class RoleDoesNotExist(RoleError):
    def __str__(self) -> str:
        return f"Role with id '{self.role_id}' does not exist."


@register.exception(create_handler(400))
class RoleAlreadyExists(RoleError):
    def __init__(self, role_name: str) -> None:
        self.role_name = role_name

    def __str__(self) -> str:
        return f"Role with name '{self.role_name}' already exists."
