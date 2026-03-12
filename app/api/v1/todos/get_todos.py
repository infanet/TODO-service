from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import TodoResponse
from db import get_async_session
from services import TodoService

router = APIRouter()


@router.get("/all", response_model=list[TodoResponse])
async def handle_get_todos(session: AsyncSession = Depends(get_async_session)):
    return await TodoService(session).get_todos()
