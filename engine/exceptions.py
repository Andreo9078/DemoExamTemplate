from typing import Optional, Any


class PermissionDenied(Exception):
    pass


class ObjectDoesNotExist(Exception):
    def __init__(
        self,
        object_id: Optional[Any] = None,
        object_class_name: Optional[str] = None,
    ) -> None:
        self.object_class_name = object_class_name
        self.object_id = object_id

    def __str__(self) -> str:
        if self.object_class_name and self.object_id:
            return f"Object {self.object_class_name} with id '{self.object_id}' does not exist."
        elif self.object_id:
            return f"Object with id '{self.object_id}' does not exist."
        else:
            return "Object does not exist."
