from sqlalchemy.ext.asyncio import AsyncSession

from repositories import (
    TodoRepositories,
    CategoryRepository,
    UserRepository,
)


class TodoService:
    def __init__(self, session: AsyncSession):
        self.user_repositories = UserRepository(session)
        self.category_repositories = CategoryRepository(session)
        self.todo_repositories = TodoRepositories(session)

    async def get_todos(self):
        return await self.todo_repositories.get_all()
