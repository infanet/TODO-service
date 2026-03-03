from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

from db import Base


class TodoTags(Base):
    __tablename__ = "todo_tags"

    __table_args__ = (PrimaryKeyConstraint("todo_id", "tag_id"),)

    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    todos_todo: Mapped["Todo"] = relationship(
        "Todo",
        back_populates="items",
    )
