from fastapi import APIRouter

from . import get_users, get_user, delete_user

router_users = APIRouter()

router_users.include_router(get_users.router)
router_users.include_router(get_user.router)
router_users.include_router(delete_user.router)
