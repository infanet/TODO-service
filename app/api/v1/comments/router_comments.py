from fastapi import APIRouter

from . import (
    get_comments,
    get_comment,
    post_comment,
    put_comment,
    delete_comment,
)

router_comments = APIRouter()

router_comments.include_router(get_comments.router)
router_comments.include_router(get_comment.router)
router_comments.include_router(post_comment.router)
router_comments.include_router(put_comment.router)
router_comments.include_router(delete_comment.router)
