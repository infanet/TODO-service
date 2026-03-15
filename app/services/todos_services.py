from sqlalchemy.ext.asyncio import AsyncSession

from repositories import TodoRepositories
from services import UserService, CategoryService
from core import AllError, ErrorMessages
from schemas import TodoPatch


class TodoService:
    def __init__(self, session: AsyncSession):
        self.user_services = UserService(session)
        self.category_services = CategoryService(session)
        self.todo_repositories = TodoRepositories(session)

    async def get_404_not_found(self, todo_id: int):
        todo = await self.todo_repositories.get_by_id(todo_id)
        if not todo:
            raise AllError(ErrorMessages.TODO_404).not_found()
        return todo

    async def get_todos(self):
        return await self.todo_repositories.get_all()

    async def get_todo(self, user_id: int, category_id: int, todo_id: int):
        await self.user_services.get_404_not_found(user_id)
        await self.category_services.get_404_not_found(category_id)
        await self.get_404_not_found(todo_id)
        return await self.todo_repositories.get_id_user_with_category_with_todo(
            user_id=user_id, category_id=category_id, todo_id=todo_id
        )

    async def create_todo(self, user_id, category_id, todo):
        await self.user_services.get_404_not_found(user_id)
        await self.category_services.get_404_not_found(category_id)

        return await self.todo_repositories.create(
            user_id=user_id, category_id=category_id, todo=todo
        )

    async def patch_todo(
        self,
        user_id: int,
        category_id: int,
        todo_id: int,
        new_todo: TodoPatch,
    ):
        await self.user_services.get_404_not_found(user_id)
        await self.category_services.get_404_not_found(category_id)
        todo = await self.get_404_not_found(todo_id)

        return await self.todo_repositories.patch(todo=todo, new_todo=new_todo)

    async def delete_todo(self, todo_id: int):
        todo = await self.get_404_not_found(todo_id)

        await self.todo_repositories.del_todo(todo)

        return todo
