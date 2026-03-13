from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Todo


class TodoRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        return (await self.session.scalars(select(Todo))).all()
