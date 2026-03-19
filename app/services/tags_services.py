from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import TagRepositories
from services import UserService, TodoService
from schemas import TagCreate, TagPatch
from core import AllError, ErrorMessages


class TagService:
    def __init__(self, session: AsyncSession):
        self.todo_services = TodoService(session)
        self.user_services = UserService(session)
        self.tag_repositories = TagRepositories(session)

    async def get_404_not_found(self, tag_id: int):
        tag = await self.tag_repositories.get_by_id(tag_id)
        if not tag:
            raise AllError(ErrorMessages.TAG_404).not_found()
        return tag

    async def get_tags(self, todo_id: int, user: User):
        todo = await self.todo_services.get_404_not_found(todo_id)

        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )

        return await self.tag_repositories.get_all(todo_id=todo_id, user=user)

    async def get_tag(self, user: User, tag_id: int, todo_id: int):
        todo = await self.todo_services.get_404_not_found(todo_id)

        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )

        tag = await self.get_404_not_found(tag_id)

        await self.user_services.check_current(
            data_id=tag.user_id, current_user_id=user.id
        )

        return await self.tag_repositories.get_tag_user(
            user=user, tag_id=tag_id, todo_id=todo_id
        )

    async def create_tag(self, todo_id: int, user: User, tag: TagCreate):
        todo = await self.todo_services.get_404_not_found(todo_id)

        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )

        return await self.tag_repositories.create(todo_id=todo_id, user=user, tag=tag)

    async def patch_tag(self, user: User, tag_id: int, new_tag: TagPatch):

        tag = await self.get_404_not_found(tag_id)

        await self.user_services.check_current(
            data_id=tag.user_id, current_user_id=user.id
        )

        return await self.tag_repositories.patch(new_tag=new_tag, tag=tag)

    async def delete_tag(self, tag_id: int, user: User):
        tag = await self.get_404_not_found(tag_id)

        await self.user_services.check_current(
            data_id=tag.user_id, current_user_id=user.id
        )
        await self.tag_repositories.del_tag(tag)

        return tag
