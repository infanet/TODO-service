# register()
#         → проверить что email не занят (через user_repo)
#         → проверить что username не занят (через user_repo)
#         → хэшировать пароль
#         → создать пользователя (через user_repo)
#         → вернуть UserResponse
#
#     login()
#         → найти пользователя по email (через user_repo)
#         → проверить пароль (bcrypt)
#         → создать access_token + refresh_token
#         → сохранить refresh_token (через refresh_token_repo)
#         → вернуть TokenResponse
#
#     refresh()
#         → декодировать refresh_token
#         → найти токен в БД (через refresh_token_repo)
#         → проверить что не отозван и не истёк
#         → отозвать старый токен
#         → создать новую пару токенов
#         → вернуть TokenResponse
#
#     logout()
#         → найти refresh_token в БД
#         → пометить is_revoked = True          (отозвать refresh token)

from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserRepository, RefreshTokenRepository
from schemas import UserCreate, UserResponse
from schemas import TokenResponse, LoginRequest, RefreshRequest
from models import RefreshToken, User
from core import (
    AllError,
    ErrorMessages,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
import jwt


class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)
        self.refresh_token_repository = RefreshTokenRepository(session)

    async def register(self, user: UserCreate) -> UserResponse:
        if await self.user_repository.get_by_email(str(user.email)):
            raise AllError(ErrorMessages.USER_400).bad_request()
        hashed = hash_password(user.password)
        return await self.user_repository.create(user=user, hashed_password=hashed)

    async def login(self, login_user: LoginRequest) -> TokenResponse:
        user: User = await self.user_repository.get_by_email(str(login_user.email))
        if not user or not verify_password(login_user.password, user.hashed_password):
            raise AllError("Invalid email or password").bad_request()

        access_token = create_access_token(user.id)
        refresh_token, expires_at = create_refresh_token(user.id)

        await self.refresh_token_repository.create(
            user_id=user.id,
            token=refresh_token,
            expires_at=expires_at,
        )
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_user: RefreshRequest) -> TokenResponse:
        # 1. декодируем токен (jwt проверит подпись и срок)
        try:
            payload = decode_token(refresh_user.refresh_token)
        except jwt.ExpiredSignatureError:
            raise AllError("Refresh token expired").bad_request()
        except jwt.InvalidTokenError:
            raise AllError("Invalid refresh token").bad_request()

        # 2. ищем в БД — он должен существовать и не быть отозван
        refresh_token: RefreshToken | None = (
            await self.refresh_token_repository.get_by_token(refresh_user.refresh_token)
        )
        if not refresh_token or refresh_token.is_revoked:
            raise AllError("Refresh token is revoked or not found").bad_request()

        # 3. отзываем старый токен
        await self.refresh_token_repository.revoke(refresh_token)

        # 4. выдаём новую пару
        user_id = int(payload["sub"])
        access_token = create_access_token(user_id)
        new_refresh_token, expires_at = create_refresh_token(user_id)

        await self.refresh_token_repository.create(
            user_id=user_id,
            token=new_refresh_token,
            expires_at=expires_at,
        )
        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

    async def logout(self, refresh_user: RefreshRequest) -> None:
        refresh_token: RefreshToken | None = (
            await self.refresh_token_repository.get_by_token(refresh_user.refresh_token)
        )
        if refresh_token and not refresh_token.is_revoked:
            await self.refresh_token_repository.revoke(refresh_token)
