from fastapi import APIRouter

from . import (
    get_categories,
    get_category,
    post_category,
    patch_category,
    delete_category,
)

router_categories = APIRouter()

router_categories.include_router(get_categories.router)

router_categories.include_router(get_category.router)
router_categories.include_router(post_category.router)
router_categories.include_router(patch_category.router)
router_categories.include_router(delete_category.router)
