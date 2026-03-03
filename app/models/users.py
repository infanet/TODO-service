from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    todo: Mapped[list["Todo"]] = relationship(
        "Todo",
        back_populates="user_todos",
        cascade="all, delete-orphan",
    )

    refresh_token: Mapped["RefreshToken"] = relationship(
        "RefreshToken",
        back_populates="user_token",
        cascade="all, delete-orphan",
    )

    tag = Mapped[list["Tag"]] = relationship(
        "Tag",
        back_populates="user_tags",
        cascade="all, delete-orphan",
    )
