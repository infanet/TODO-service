from datetime import datetime
from pydantic import BaseModel, ConfigDict

from models.todos import Status, Priority


class TodoPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    deadline: datetime | None = None
