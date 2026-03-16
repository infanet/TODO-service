from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import TokenResponse
from services import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def handle_login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return await AuthService(session).login(form)
