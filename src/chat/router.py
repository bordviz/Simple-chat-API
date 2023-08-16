from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, and_, or_
from .models import Chat
from .schemas import ChatCreate
from message.models import Message
from database import AsyncSession, get_async_session
from sqlalchemy import exc
from auth.models import User
from auth.auth import current_user

router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)

@router.post('/create')
async def create_chat(
    body: ChatCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        if body.first_user == user.id or body.second_user == user.id:
            check = select(Chat).where(
                and_(
                    Chat.first_user.in_([body.first_user, body.second_user]),
                    Chat.second_user.in_([body.first_user, body.second_user])
                )
            )
            res = await session.execute(check)
            if res.scalars().all() == []:
                query = insert(Chat).values(**body.model_dump())
                await session.execute(query)
                await session.commit()
                return {'status': 'success', 'message': 'Chat created successfully'}
            raise HTTPException(status_code=405, detail='Chat already created')
        raise HTTPException(status_code=400, detail='You cannot create a chat in which you are not yourself')
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail='This user does not exist')

@router.get('/all-chats')
async def get_user_chats(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query =  select(Chat).where(
        or_(
            Chat.first_user == user.id,
            Chat.second_user == user.id,
        )
    )
    res = await session.execute(query)
    return res.scalars().all()
    