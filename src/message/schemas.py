from pydantic import BaseModel, Field
from datetime import datetime

class MessageSend(BaseModel):
    message: str
    chat_id: int

class LastMessages(BaseModel):
    limit: int = Field(gt=-1, default=10)
    skip: int = Field(gt=-1, default=0)
    chat_id: int

class MessageRead(BaseModel):
    id: int
    chat_id: int
    sender: int
    message: str
    send_time: datetime