from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, func, DateTime

from db import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    color: Mapped[str] = mapped_column(String(7))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    ######################################################
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user_categories: Mapped["User"] = relationship(
        "User",
        back_populates="categories",
    )

    #####################################################
    todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        back_populates="category_todos",
        cascade="all, delete-orphan",
    )
