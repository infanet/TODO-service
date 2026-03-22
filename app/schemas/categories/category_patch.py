from pydantic import BaseModel


class CategoryPatch(BaseModel):
    name: str | None = None
    color: str | None = None
