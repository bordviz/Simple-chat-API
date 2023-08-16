from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from auth.models import User

class Chat(Base):
    __tablename__ = 'chat'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_user = Column(Integer, ForeignKey(User.id), nullable=False)
    second_user = Column(Integer, ForeignKey(User.id), nullable=False)
    sender = Column(Integer, ForeignKey(User.id))
    message = Column(String)
    send_time = Column(TIMESTAMP)

