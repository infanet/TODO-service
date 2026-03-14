from sqlalchemy.ext.asyncio import AsyncSession

from repositories import (
    CommentRepositories,
    TodoRepositories,
    UserRepository,
)
from schemas import CommentCreate
from core import AllError, ErrorMessages


class CommentService:
    def __init__(self, session: AsyncSession):
        self.user_repositories = UserRepository(session)
        self.todo_repositories = TodoRepositories(session)
        self.comment_repositories = CommentRepositories(session)

    async def get_comments(self):
        return await self.comment_repositories.get_all()

    async def get_item(self, user_id: int, todo_id: int, comment_id: int):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()
        todo = await self.todo_repositories.get_by_id(todo_id)
        if not todo:
            raise AllError(ErrorMessages.TODO_404).not_found()
        comment = await self.comment_repositories.get_by_id(comment_id)
        if not comment:
            raise AllError(ErrorMessages.COMMENT_404).not_found()

        return await self.comment_repositories.get_user_with_todo_with_comment(
            user_id=user_id, todo_id=todo_id, comment_id=comment_id
        )

    async def create_comment(self, user_id: int, todo_id: int, comment: CommentCreate):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()
        todo = await self.todo_repositories.get_by_id(todo_id)
        if not todo:
            raise AllError(ErrorMessages.TODO_404).not_found()

        return await self.comment_repositories.create(
            user_id=user_id, todo_id=todo_id, comment=comment
        )

    async def update_comment(
        self, user_id: int, todo_id: int, comment_id: int, new_comment: CommentCreate
    ):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()
        todo = await self.todo_repositories.get_by_id(todo_id)
        if not todo:
            raise AllError(ErrorMessages.TODO_404).not_found()
        comment = await self.comment_repositories.get_by_id(comment_id)
        if not comment:
            raise AllError(ErrorMessages.COMMENT_404).not_found()

        return await self.comment_repositories.up_comment(
            comment=comment, new_comment=new_comment
        )

    async def delete_comment(self, comment_id: int):
        comment = await self.comment_repositories.get_by_id(comment_id)
        if not comment:
            raise AllError(ErrorMessages.COMMENT_404).not_found()

        await self.comment_repositories.del_comment(comment)

        return comment
