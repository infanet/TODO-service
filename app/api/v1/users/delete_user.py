from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from services import UserService
from schemas import UserResponse

router = APIRouter()


@router.delete("/delete", response_model=UserResponse)
async def handle_delete_user(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await UserService(session).delete_user(user_id)
