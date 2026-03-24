from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import TodoRepositories
from services import UserService, CategoryService
from core import AllError, ErrorMessages, get_logger
from schemas import TodoPatch, TodoCreate


logger = get_logger(__name__)

class TodoService:
    def __init__(self, session: AsyncSession):
        self.user_services = UserService(session)
        self.category_services = CategoryService(session)
        self.todo_repositories = TodoRepositories(session)

    async def get_404_not_found(self, todo_id: int):
        todo = await self.todo_repositories.get_by_id(todo_id)
        if not todo:
            logger.warning("Нет задачи с таким индексом %s", todo_id)
            raise AllError(ErrorMessages.TODO_404).not_found()
        return todo

    async def get_todos(self, category_id: int, user: User):
        category = await self.category_services.get_404_not_found(category_id)

        await self.user_services.check_current(
            data_id=category.user_id, current_user_id=user.id
        )

        return await self.todo_repositories.get_all(category_id=category_id, user=user)

    async def get_todo(self, user: User, category_id: int, todo_id: int):
        category = await self.category_services.get_404_not_found(category_id)

        await self.user_services.check_current(
            data_id=category.user_id, current_user_id=user.id
        )

        todo = await self.get_404_not_found(todo_id)

        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )

        return await self.todo_repositories.get_id_user_with_category_with_todo(
            user=user, category_id=category_id, todo_id=todo_id
        )

    async def create_todo(self, user: User, category_id: int, todo: TodoCreate):
        category = await self.category_services.get_404_not_found(category_id)

        await self.user_services.check_current(
            data_id=category.user_id, current_user_id=user.id
        )

        return await self.todo_repositories.create(
            user=user, category_id=category_id, todo=todo
        )

    async def patch_todo(
        self,
        user: User,
        category_id: int,
        todo_id: int,
        new_todo: TodoPatch,
    ):
        category = await self.category_services.get_404_not_found(category_id)

        await self.user_services.check_current(
            data_id=category.user_id, current_user_id=user.id
        )

        todo = await self.get_404_not_found(todo_id)

        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )

        return await self.todo_repositories.patch(todo=todo, new_todo=new_todo)

    async def delete_todo(self, todo_id: int, user: User):
        todo = await self.get_404_not_found(todo_id)

        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )

        await self.todo_repositories.del_todo(todo)

        return todo
