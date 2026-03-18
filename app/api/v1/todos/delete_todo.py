from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from models import User
from schemas import TodoResponse
from db import get_async_session
from services import TodoService

router = APIRouter()


@router.delete("/delete", response_model=TodoResponse)
async def handle_delete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await TodoService(session).delete_todo(
        todo_id=todo_id, user_id=current_user.id
    )
