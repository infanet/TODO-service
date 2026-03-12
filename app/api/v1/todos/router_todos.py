from fastapi import APIRouter

from . import (
    get_todos,
    get_todo,
    post_todo,
    patch_todo,
    delete_todo,
)

router_todos = APIRouter()

router_todos.include_router(get_todos.router)
router_todos.include_router(get_todo.router)
router_todos.include_router(post_todo.router)
router_todos.include_router(patch_todo.router)
router_todos.include_router(delete_todo.router)
