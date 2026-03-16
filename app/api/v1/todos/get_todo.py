from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import TodoItems
from db import get_async_session
from services import TodoService

router = APIRouter()


@router.get("/one", response_model=TodoItems)
async def handle_get_todo(
    user_id: int,
    category_id: int,
    todo_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await TodoService(session).get_todo(
        user_id=user_id, category_id=category_id, todo_id=todo_id
    )
