from pydantic import ConfigDict

from .tag_base import TagBase
from schemas import UserResponse, TodoResponse


class TagResponse(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TodoTagResponse(TodoResponse):
    t_tags: list[TagResponse]


class TagItem(UserResponse):
    todos: list[TodoTagResponse]
