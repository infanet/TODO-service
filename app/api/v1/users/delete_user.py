from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from services import UserService
from schemas import UserResponse

router = APIRouter()


@router.delete("/delete", response_model=UserResponse)
async def handle_delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await UserService(session).delete_user(user_id)
