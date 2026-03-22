from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import UserCreate, UserResponse
from services import AuthService

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def handle_register(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await AuthService(session).register(user)
