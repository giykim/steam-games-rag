from fastapi import APIRouter

from api.models.chat_request import ChatRequest
from api.models.chat_response import ChatResponse
from api.chat.anthropic_chat_service import AnthropicChatService


class ChatRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/chat", self.chat, methods=["POST"], response_model=ChatResponse)
        self.service = AnthropicChatService()

    def chat(self, request: ChatRequest) -> ChatResponse:
        return self.service.chat(request.messages)
