from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import CommentResponse
from services import CommentService

router = APIRouter()


@router.get("/all", response_model=list[CommentResponse])
async def handle_get_comments(session: AsyncSession = Depends(get_async_session)):
    return await CommentService(session).get_comments()
