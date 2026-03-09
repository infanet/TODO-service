from sqlalchemy import ForeignKey, Column, Table

from app.db import Base

todo_tags = Table(
    "todo_tags",
    Base.metadata,
    Column(
        "todo_id",
        ForeignKey("todos.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
