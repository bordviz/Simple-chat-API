from pydantic import BaseModel
from datetime import datetime

class ChatCreate(BaseModel):
    first_user: int
    second_user: int

class ChatRead(ChatCreate):
    id: int
