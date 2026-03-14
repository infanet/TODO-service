from pydantic import ConfigDict

from .todo_base import TodoBase
from schemas import UserResponse, CategoryResponse


class TodoResponse(TodoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TodosCategory(CategoryResponse):
    todos: list[TodoResponse]


class TodoItems(UserResponse):
    categories: list[TodosCategory]
