from pydantic import BaseModel

from api.models.message import Message


class ChatRequest(BaseModel):
    session_id: str
    message: Message
