from fastapi import APIRouter

from .users import router_users

router = APIRouter(prefix="/api/v1")

router.include_router(router_users, prefix="/users", tags=["users"])
