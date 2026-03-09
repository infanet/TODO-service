import enum
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, TEXT, Enum as SAEnum, func, DateTime, String

from app.db import Base
from app.models.todo_tags import todo_tags


class Status(enum.Enum):
    todo = "todo"
    done = "done"
    in_progress = "in_progress"


class Priority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(TEXT)
    status: Mapped[Status] = mapped_column(
        SAEnum(Status), default=Status.todo, server_default="todo"
    )
    priority: Mapped[Priority] = mapped_column(
        SAEnum(Priority), default=Priority.medium, server_default="medium"
    )
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    ############################################################################
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user_todos: Mapped["User"] = relationship(
        "User",
        back_populates="todos",
    )

    ############################################################################
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=True
    )

    category_todos: Mapped["Category | None"] = relationship(
        "Category",
        back_populates="todos",
    )

    ############################################################################
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="todo_comments",
        cascade="all, delete-orphan",
    )

    ##########################################################################
    t_tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=todo_tags,
        back_populates="t_todos",
    )
