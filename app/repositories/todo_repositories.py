from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Todo


class TodoRepositories:
    def __init__(self, session: AsyncSession):
        self.todo_repositories = session

    async def get_all(self):
        return (await self.todo_repositories.scalars(select(Todo))).all()
