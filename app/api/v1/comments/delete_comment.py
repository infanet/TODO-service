from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import CommentResponse
from services import CommentService

router = APIRouter()


@router.delete("/delete", response_model=CommentResponse)
async def handle_delete_comment(
    comment_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await CommentService(session).delete_comment(comment_id)
