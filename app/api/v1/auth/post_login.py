from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import TokenResponse, LoginRequest
from services import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def handle_login(
    login_user: LoginRequest, session: AsyncSession = Depends(get_async_session)
):
    return await AuthService(session).login(login_user)
