from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import CommentResponse
from services import CommentService

router = APIRouter()


@router.delete("/delete", response_model=CommentResponse)
async def handle_delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await CommentService(session).delete_comment(
        comment_id=comment_id, user=current_user
    )
