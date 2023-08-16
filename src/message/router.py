from typing import List
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends, HTTPException
from .schemas import MessageSend, MessageRead, LastMessages
from .manager import ConnectionManager
from .models import Message
from auth.models import User
from auth.auth import current_user
from database import AsyncSession, get_async_session
from sqlalchemy import select
from chat.models import Chat
from chat.schemas import ChatRead

router = APIRouter(
    prefix='/message',
    tags=['Message']
)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            mes = MessageSend(**data)
            print(mes.message)
            await manager.send_personal_message(
                message=mes.message, 
                chat_id=mes.chat_id, 
                user_id=user_id,
                websocket=websocket
            )
            await manager.broadcast(
                message=mes.message, 
                chat_id=mes.chat_id, 
                user_id=user_id
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.post('/last-messages')
async def get_last_messages(
    body: LastMessages,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> List[MessageRead]:
    check = select(Chat).where(Chat.id == body.chat_id)
    check_res = await session.execute(check)
    is_chat_member: ChatRead = check_res.scalar_one()
    if user.id == is_chat_member.first_user or user.id == is_chat_member.second_user:
        query = select(Message).where(Message.chat_id == body.chat_id).order_by(Message.send_time.desc()).offset(body.skip).limit(body.limit)
        res = await session.execute(query)
        return res.scalars().all()
    raise HTTPException(status_code=400, detail='You are not a member of this chat')