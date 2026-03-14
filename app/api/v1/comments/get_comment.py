from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import CommentItemResponse
from services import CommentService

router = APIRouter()


@router.get("/item", response_model=CommentItemResponse)
async def handle_get_item(
    user_id: int,
    todo_id: int,
    comment_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await CommentService(session).get_item(
        user_id=user_id, todo_id=todo_id, comment_id=comment_id
    )
