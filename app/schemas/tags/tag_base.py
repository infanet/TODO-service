from pydantic import BaseModel, Field, field_validator


class TagBase(BaseModel):
    name: str
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")

    @field_validator("name")
    def check_name(cls, n: str) -> str:  # type: ignore[misc]
        if any(char.isdigit() for char in n):
            raise ValueError("Name cannot contain digits")
        return n
