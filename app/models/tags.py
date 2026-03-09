from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, String, text, func, DateTime

from db import Base
from .todo_tags import todo_tags


class Tag(Base):
    __tablename__ = "tags"

    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(
        String(7), default="#10b981", server_default=text("'#10b981'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    ######################################################################
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user_tags: Mapped["User"] = relationship(
        "User",
        back_populates="tags",
    )

    ######################################################################
    t_todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        secondary=todo_tags,
        back_populates="t_tags",
    )
