from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import CommentRepositories
from services import UserService, TodoService
from schemas import CommentCreate
from core import AllError, ErrorMessages


class CommentService:
    def __init__(self, session: AsyncSession):
        self.user_services = UserService(session)
        self.todo_services = TodoService(session)
        self.comment_repositories = CommentRepositories(session)

    async def get_404_not_found(self, comments_id: int):
        comments = await self.comment_repositories.get_by_id(comments_id)
        if not comments:
            raise AllError(ErrorMessages.COMMENT_404).not_found()
        return comments

    async def get_comments(self, todo_id: int, user: User):
        todo = await self.todo_services.get_404_not_found(todo_id)
        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )
        return await self.comment_repositories.get_all(
            todo_id=todo_id,
            user=user,
        )

    async def get_item(self, user: User, todo_id: int, comment_id: int):
        comment = await self.get_404_not_found(comment_id)
        await self.user_services.check_current(
            data_id=comment.user_id, current_user_id=user.id
        )
        todo = await self.todo_services.get_404_not_found(todo_id)
        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )

        return await self.comment_repositories.get_user_with_todo_with_comment(
            user=user, todo_id=todo_id, comment_id=comment_id
        )

    async def create_comment(
        self,
        user: User,
        todo_id: int,
        comment: CommentCreate,
    ):
        todo = await self.todo_services.get_404_not_found(todo_id)

        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )

        return await self.comment_repositories.create(
            user=user, todo_id=todo_id, comment=comment
        )

    async def update_comment(
        self,
        user: User,
        todo_id: int,
        comment_id: int,
        new_comment: CommentCreate,
    ):
        todo = await self.todo_services.get_404_not_found(todo_id)
        await self.user_services.check_current(
            data_id=todo.user_id, current_user_id=user.id
        )
        comment = await self.get_404_not_found(comment_id)
        await self.user_services.check_current(
            data_id=comment.user_id, current_user_id=user.id
        )

        return await self.comment_repositories.up_comment(
            comment=comment, new_comment=new_comment
        )

    async def delete_comment(self, comment_id: int, user: User):
        comment = await self.get_404_not_found(comment_id)

        await self.user_services.check_current(
            data_id=comment.user_id, current_user_id=user.id
        )

        await self.comment_repositories.del_comment(comment)

        return comment
