from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, with_loader_criteria

from models import Comment, User, Todo
from schemas import CommentCreate


class CommentRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, todo_id: int, user: User):
        result = await self.session.execute(
            select(User)
            .options(
                selectinload(User.todos).selectinload(Todo.comments),
                with_loader_criteria(Todo, Todo.id == todo_id),
            )
            .where(User.id == user.id)
        )
        return result.scalar_one()

    async def get_by_id(self, comment_id: int):
        return (
            await self.session.execute(select(Comment).where(Comment.id == comment_id))
        ).scalar_one_or_none()

    async def get_user_with_todo_with_comment(
        self, user: User, todo_id: int, comment_id: int
    ):
        item = await self.session.execute(
            select(User)
            .options(
                selectinload(User.todos).selectinload(Todo.comments),
                with_loader_criteria(Todo, Todo.id == todo_id),
                with_loader_criteria(Comment, Comment.id == comment_id),
            )
            .where(User.id == user.id)
        )
        return item.scalar_one_or_none()

    async def create(self, user: User, todo_id: int, comment: CommentCreate):
        new_comment = Comment(**comment.model_dump(), user_id=user.id, todo_id=todo_id)
        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)
        return new_comment

    async def up_comment(self, comment: Comment, new_comment: CommentCreate):
        update_data = new_comment.model_dump()

        for key, value in update_data.items():
            setattr(comment, key, value)

        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def del_comment(self, comment):
        await self.session.delete(comment)
        await self.session.commit()
