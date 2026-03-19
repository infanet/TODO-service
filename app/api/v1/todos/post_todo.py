from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from models import User
from schemas import TodoResponse, TodoCreate
from services import TodoService
from db import get_async_session

router = APIRouter()


@router.post("/create", response_model=TodoResponse)
async def handle_create_todo(
    category_id: int,
    todo: TodoCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await TodoService(session).create_todo(
        user=current_user, category_id=category_id, todo=todo
    )
