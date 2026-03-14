from fastapi import APIRouter

from . import (
    get_tags,
    get_tag,
    post_tag,
    patch_tag,
    delete_tag,
)

router_tags = APIRouter()

router_tags.include_router(get_tags.router)
router_tags.include_router(get_tag.router)
router_tags.include_router(post_tag.router)
router_tags.include_router(patch_tag.router)
router_tags.include_router(delete_tag.router)
