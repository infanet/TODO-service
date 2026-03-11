from pydantic import BaseModel, ConfigDict


class CategoryPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str | None = None
    color: str | None = None
