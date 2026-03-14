from pydantic import BaseModel


class TagPatch(BaseModel):
    name: str | None = None
    color: str | None = None
