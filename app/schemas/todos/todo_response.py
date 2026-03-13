from pydantic import ConfigDict

from .todo_base import TodoBase


class TodoResponse(TodoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
