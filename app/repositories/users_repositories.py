from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def all_users(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()
