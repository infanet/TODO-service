from pydantic import ConfigDict

from .comment_base import CommentBase
from schemas import UserResponse, TodoResponse


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TodoComment(TodoResponse):
    comments: list[CommentResponse]


class CommentItemResponse(UserResponse):
    todos: list[TodoComment]
