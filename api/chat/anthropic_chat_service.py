import logging

import anthropic

from api.chat.chat_service import ChatService
from api.models.message import Message
from config import ANTHROPIC_API_KEY


class AnthropicChatService(ChatService):
    CHAT_SERVICE = "claude-sonnet-4-6"

    def __init__(self):
        super().__init__()
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def _generate_response(self, messages: list[dict], context: str) -> str:
        recent_messages = messages[-self.MAX_HISTORY:]
        
        response = self.client.messages.create(
            model=self.CHAT_SERVICE,
            max_tokens=1024,
            system=self.SYSTEM_PROMPT + "\n\nContext:\n" + context,
            messages=recent_messages,
        )

        logging.info("Generated chat response.")
        return response.content[0].text
