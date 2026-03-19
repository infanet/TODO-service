from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, with_loader_criteria

from models import Todo, User, Category
from schemas import TodoCreate, TodoPatch


class TodoRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, category_id: int, user: User):
        return (
            await self.session.execute(
                select(User)
                .options(
                    selectinload(User.categories).selectinload(Category.todos),
                    with_loader_criteria(Category, Category.id == category_id),
                )
                .where(User.id == user.id)
            )
        ).scalar_one()

    async def get_by_id(self, todo_id):
        todo = await self.session.execute(select(Todo).where(Todo.id == todo_id))
        return todo.scalar_one_or_none()

    async def get_id_user_with_category_with_todo(
        self, user: User, category_id: int, todo_id: int
    ):
        todo = await self.session.execute(
            select(User)
            .options(
                selectinload(User.categories).selectinload(Category.todos),
                with_loader_criteria(Category, Category.id == category_id),
                with_loader_criteria(Todo, Todo.id == todo_id),
            )
            .where(User.id == user.id)
        )
        return todo.scalar_one()

    async def create(self, user: User, category_id: int, todo: TodoCreate):
        new_todo = Todo(**todo.model_dump(), user_id=user.id, category_id=category_id)
        self.session.add(new_todo)
        await self.session.commit()
        await self.session.refresh(new_todo)
        return new_todo

    async def patch(self, todo, new_todo: TodoPatch):
        update_data = new_todo.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(todo, key, value)

        await self.session.commit()
        await self.session.refresh(todo)

        return todo

    async def del_todo(self, todo):
        await self.session.delete(todo)
        await self.session.commit()
