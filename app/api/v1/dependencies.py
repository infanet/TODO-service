# защита маршрутов
from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from db import get_async_session
from repositories import UserRepository
from core import decode_token, AllError

bearer_scheme = HTTPBearer()  # читает заголовок: Authorization: Bearer <token>


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise AllError("Token expired").unauthorized()
    except jwt.InvalidTokenError:
        raise AllError("Invalid token").unauthorized()

    user_id = int(payload["sub"])
    user = await UserRepository(session).get_by_id(user_id)
    if not user:
        raise AllError("User not found").unauthorized()

    return user
