from pydantic import BaseModel

from api.models.message import Message


class ChatResponse(BaseModel):
    message: Message
