from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User
from schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        return (await self.session.scalars(select(User))).all()

    async def get_by_id(self, user_id: int):
        """не трогать оно относится к v1/dependencies.py"""
        return (
            await self.session.execute(select(User).where(User.id == user_id))
        ).scalar_one_or_none()

    async def get_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate, hashed_password: str):
        new_user = User(
            username=user.username,
            email=str(user.email),
            hashed_password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def del_user(self, user):
        await self.session.delete(user)
        await self.session.commit()
