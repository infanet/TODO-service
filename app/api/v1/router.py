from fastapi import APIRouter

from .users import router_users
from .categories import router_categories

router = APIRouter(prefix="/api/v1")

router.include_router(router_users, prefix="/users", tags=["users"])
router.include_router(router_categories, prefix="/categories", tags=["categories"])
