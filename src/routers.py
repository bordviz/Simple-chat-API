from message.router import router as router_message
from chat.router import router as router_chat
from user.router import router as router_user

all_routers = [
    router_user,
    router_chat,
    router_message,
]