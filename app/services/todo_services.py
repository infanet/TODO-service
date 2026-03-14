from sqlalchemy.ext.asyncio import AsyncSession

from repositories import (
    TodoRepositories,
    CategoryRepository,
    UserRepository,
)
from core import AllError, ErrorMessages


class TodoService:
    def __init__(self, session: AsyncSession):
        self.user_repositories = UserRepository(session)
        self.category_repositories = CategoryRepository(session)
        self.todo_repositories = TodoRepositories(session)

    async def get_todos(self):
        return await self.todo_repositories.get_all()

    async def get_todo(self, user_id: int, category_id: int, todo_id: int):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()
        category = await self.category_repositories.get_by_id(category_id)
        if not category:
            raise AllError(ErrorMessages.CATEGORY_404).not_found()
        todo = await self.todo_repositories.get_by_id(todo_id)
        if not todo:
            raise AllError(ErrorMessages.TODO_404).not_found()
        return await self.todo_repositories.get_id_user_with_category_with_todo(
            user_id=user_id, category_id=category_id, todo_id=todo_id
        )

    async def create_todo(self, user_id, category_id, todo):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()

        category = await self.category_repositories.get_by_id(category_id)
        if not category:
            raise AllError(ErrorMessages.CATEGORY_404).not_found()

        return await self.todo_repositories.create(
            user_id=user_id, category_id=category_id, todo=todo
        )
