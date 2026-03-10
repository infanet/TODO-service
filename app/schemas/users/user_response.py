from pydantic import ConfigDict

from user_base import UserBase


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
