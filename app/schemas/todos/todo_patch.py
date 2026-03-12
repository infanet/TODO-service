from datetime import datetime
from pydantic import BaseModel

from models.todos import Status, Priority


class TodoPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    deleted: datetime | None = None
