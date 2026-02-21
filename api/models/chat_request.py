from pydantic import BaseModel

from api.models.message import Message


class ChatRequest(BaseModel):
    messages: list[Message]
