from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import UserCreate, UserResponse
from services import UserService

router = APIRouter()


@router.post(
    "/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def handle_create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    result = await UserService(session).create_user(user)
    return result
