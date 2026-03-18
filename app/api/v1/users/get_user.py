from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import UserResponse
from services import UserService

router = APIRouter()


@router.get("/one", response_model=UserResponse)
async def handle_get_user(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await UserService(session).get_user(current_user)
