from database import async_session_maker
from sqlalchemy import insert, select, update
from fastapi import WebSocket
from .models import Message
from chat.models import Chat
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, chat_id: int, user_id: int, websocket: WebSocket):
        await websocket.send_json({
            "message": message,
            "user_id": user_id,
            "chat_id": chat_id
        })

    async def broadcast(self, message: str, chat_id: int, user_id: int):
        await self.add_to_database(message=message, chat_id=chat_id, sender=user_id)
        recipient = await self.get_chat_members(chat_id=chat_id, user_id=user_id)
        for connection in self.active_connections:
            id = int(connection.url.query.split('user_id=')[1])
            if id == recipient:
                await connection.send_json({
                    "message": message,
                    "user_id": user_id,
                    "chat_id": chat_id
                })

    @staticmethod
    async def add_to_database(message: str, chat_id: int, sender: int):
        async with async_session_maker() as session:
            query = [insert(Message).values(
                message=message, chat_id=chat_id, sender=sender
            ), update(Chat).where(Chat.id == chat_id).values(sender=sender, send_time=datetime.now(), message=message)]
            await session.execute(query[0])
            await session.execute(query[1])
            await session.commit()

    @staticmethod
    async def get_chat_members(chat_id: int, user_id: int) -> int:
        async with async_session_maker() as session:
            query = select(Chat).where(Chat.id == chat_id)
            res = await session.execute(query)
            model: Chat = res.scalar()
            return model.first_user if model.first_user != user_id else model.second_user