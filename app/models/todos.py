import enum
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, TEXT, text, Enum as SAEnum, func, DateTime

from db import Base


class Priority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(TEXT)
    is_completed: Mapped[bool] = mapped_column(
        default=False, server_default=text("false")
    )
    priority: Mapped[Priority] = mapped_column(
        SAEnum(Priority), default=Priority.medium, server_default="medium"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="todo",
    )

    t_tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="todo_tags",
        back_populates="",
        viewonly=True,
    )

    items: Mapped["TodoTags"] = relationship(
        "TodoTags",
        back_populates="todos_todo",
        cascade="all, delete-orphan",
        single_parent=True,
    )
