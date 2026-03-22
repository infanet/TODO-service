# защита маршрутов
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from db import get_async_session
from repositories import UserRepository
from core import decode_token, AllError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise AllError("Token expired").unauthorized() from None
    except jwt.InvalidTokenError:
        raise AllError("Invalid token").unauthorized() from None

    user_id = int(payload["sub"])
    user = await UserRepository(session).get_by_id(user_id)
    if not user:
        raise AllError("User not found").unauthorized()

    return user
