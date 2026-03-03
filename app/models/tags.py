from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from db import Base


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(unique=True)

    user_tags: Mapped["User"] = relationship(
        "UserTag",
        back_populates="tag",
    )

    t_todos: Mapped[list["Tag"]] = relationship(
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
