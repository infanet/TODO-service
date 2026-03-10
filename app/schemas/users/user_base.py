from pydantic import EmailStr
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: EmailStr
