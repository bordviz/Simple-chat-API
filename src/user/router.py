from typing import List
from fastapi import APIRouter, Depends
from database import AsyncSession, get_async_session
from auth.schemas import UserRead
from sqlalchemy import select, or_
from auth.models import User

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/get-user/{user_id}')
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> UserRead:
    query = select(User).where(User.id == user_id)
    res = await session.execute(query)
    return res.scalar()

@router.get('/search')
async def searh_users(
    value: str,
    session: AsyncSession = Depends(get_async_session)
) -> List[UserRead]:
    query = select(User).where(
        or_(
            User.username.like(f'%{value}%'),
            User.email.like(f'%{value}%')
        )
    )
    res = await session.execute(query)
    return res.scalars().all()
