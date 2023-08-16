from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from auth.models import User
from chat.models import Chat

class Message(Base):
    __tablename__ = 'message'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer,  ForeignKey(Chat.id), nullable=False)
    sender = Column(Integer, ForeignKey(User.id), nullable=False)
    message = Column(String, nullable=False)
    send_time = Column(TIMESTAMP, default=datetime.utcnow)