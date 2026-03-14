from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, with_loader_criteria

from models import Todo, User, Category
from schemas import TodoCreate


class TodoRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        return (await self.session.scalars(select(Todo))).all()

    async def get_by_id(self, todo_id):
        todo = await self.session.execute(select(Todo).where(Todo.id == todo_id))
        return todo.scalar_one_or_none()

    async def get_id_user_with_category_with_todo(
        self, user_id: int, category_id: int, todo_id: int
    ):
        todo = await self.session.execute(
            select(User)
            .options(
                selectinload(User.categories).selectinload(Category.todos),
                with_loader_criteria(Category, Category.id == category_id),
                with_loader_criteria(Todo, Todo.id == todo_id),
            )
            .where(User.id == user_id)
        )
        return todo.scalar_one_or_none()

    async def create(self, user_id, category_id, todo: TodoCreate):
        new_todo = Todo(**todo.model_dump(), user_id=user_id, category_id=category_id)
        self.session.add(new_todo)
        await self.session.commit()
        await self.session.refresh(new_todo)
        return new_todo
