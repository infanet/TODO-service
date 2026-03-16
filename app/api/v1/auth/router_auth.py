from fastapi import APIRouter

from . import (
    post_register,
    post_login,
    post_refresh,
    post_logout,
)

router_auth = APIRouter()

router_auth.include_router(post_register.router)
router_auth.include_router(post_login.router)
router_auth.include_router(post_refresh.router)
router_auth.include_router(post_logout.router)
