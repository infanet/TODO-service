from pydantic import ConfigDict

from .tag_base import TagBase
from schemas import UserResponse


class TagResponse(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TagItem(UserResponse):
    tags: list[TagResponse]
