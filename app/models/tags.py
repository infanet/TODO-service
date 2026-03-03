from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from db import Base


class Tag(Base):
    __tablename__ = "tags"

    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column()

    user_tags: Mapped["User"] = relationship(
        "User",
        back_populates="tag",
    )

    t_todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        secondary="todo_tags",
        back_populates="t_tags",
        viewonly=True,
    )

    items: Mapped[list["TodoTags"]] = relationship(
        "TodoTags",
        back_populates="todos_tag",
        cascade="all, delete-orphan",
        single_parent=True,
    )
