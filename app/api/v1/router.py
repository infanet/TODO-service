from fastapi import APIRouter

from .users import router_users
from .categories import router_categories
from .todos import router_todos
from .tags import router_tags
from .comments import router_comments

router = APIRouter(prefix="/api/v1")

router.include_router(router_users, prefix="/users", tags=["users"])
router.include_router(router_categories, prefix="/categories", tags=["categories"])
router.include_router(router_todos, prefix="/todos", tags=["todos"])
router.include_router(router_tags, prefix="/tags", tags=["tags"])
router.include_router(router_comments, prefix="/comments", tags=["comments"])
