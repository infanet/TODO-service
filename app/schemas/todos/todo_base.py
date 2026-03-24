from datetime import datetime
from pydantic import BaseModel

from models.todos import Status, Priority


class TodoBase(BaseModel):
    title: str
    description: str | None = None
    status: Status = Status.todo
    priority: Priority = Priority.medium
    deadline: datetime | None = None
