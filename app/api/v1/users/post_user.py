from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_async_session
from models import User

router = APIRouter()

# @router.post("/create")
# async def create_user(user: User = Depends(get_user)):
