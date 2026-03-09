from datetime import datetime
from sqlalchemy import DateTime, func, String, TEXT, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(TEXT)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    #############################################################
    todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        back_populates="user_todos",
        cascade="all, delete-orphan",
    )

    ############################################################
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user_token",
        cascade="all, delete-orphan",
    )

    ###########################################################
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        back_populates="user_tags",
        cascade="all, delete-orphan",
    )

    ############################################################
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="user_categories",
        cascade="all, delete-orphan",
    )

    ################################################################
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user_comments",
        cascade="all, delete-orphan",
    )
