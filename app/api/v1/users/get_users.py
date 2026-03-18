from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from services import UserService
from schemas import UserResponse

router = APIRouter()


@router.get("/all", response_model=list[UserResponse])
async def handle_get_users(
    session: AsyncSession = Depends(get_async_session),
):
    return await UserService(session).get_users()
