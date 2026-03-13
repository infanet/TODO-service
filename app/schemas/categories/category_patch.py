from pydantic import BaseModel, ConfigDict


class CategoryPatch(BaseModel):
    name: str | None = None
    color: str | None = None
