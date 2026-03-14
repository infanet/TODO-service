from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import CommentResponse, CommentCreate
from services import CommentService

router = APIRouter()


@router.put("/update", response_model=CommentResponse)
async def handle_update_comment(
    user_id: int,
    todo_id: int,
    comment_id: int,
    new_comment: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await CommentService(session).update_comment(
        user_id=user_id, todo_id=todo_id, comment_id=comment_id, new_comment=new_comment
    )
