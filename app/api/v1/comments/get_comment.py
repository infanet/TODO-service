from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import CommentItemResponse
from services import CommentService

router = APIRouter()


@router.get("/item", response_model=CommentItemResponse)
async def handle_get_item(
    todo_id: int,
    comment_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await CommentService(session).get_item(
        user=current_user, todo_id=todo_id, comment_id=comment_id
    )
