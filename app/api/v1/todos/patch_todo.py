from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from models import User
from schemas import TodoResponse, TodoPatch
from services import TodoService
from db import get_async_session

router = APIRouter()


@router.patch("/patch", response_model=TodoResponse)
async def handle_patch_todo(
    category_id: int,
    todo_id: int,
    new_todo: TodoPatch,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await TodoService(session).patch_todo(
        user=current_user,
        category_id=category_id,
        todo_id=todo_id,
        new_todo=new_todo,
    )
