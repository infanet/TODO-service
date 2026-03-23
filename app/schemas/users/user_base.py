from pydantic import EmailStr, BaseModel, field_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username")
    def check_name(cls, n: str) -> str:  # type: ignore[misc]
        if any(char.isdigit() for char in n):
            raise ValueError("Username cannot contain digits")
        return n
