from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from db import Base


class TodoTags(Base):
    __tablename__ = "todo_tags"

    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    todos_todo: Mapped["Todo"] = relationship(
        "Todo",
        back_populates="items",
    )

    todos_tag: Mapped["Tag"] = relationship(
        "Tag",
        back_populates="items",
    )