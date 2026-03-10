from user_base import UserBase


class UserCreate(UserBase):

    hashed_password: str
