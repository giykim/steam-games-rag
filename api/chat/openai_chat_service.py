import logging

from openai import OpenAI

from api.chat.chat_service import ChatService
from api.models.message import Message
from config import OPENAI_API_KEY


class OpenAIChatService(ChatService):
    CHAT_SERVICE = "gpt-4o-mini"

    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def _generate_response(self, messages: list[dict], context: str) -> str:
        recent_messages = messages[-self.MAX_HISTORY:]
        
        openai_messages = [{"role": "system", "content": self.SYSTEM_PROMPT + "\n\nContext:\n" + context}]
        openai_messages += recent_messages

        response = self.client.chat.completions.create(
            model=self.CHAT_SERVICE,
            messages=openai_messages,
        )

        logging.info("Generated chat response.")
        return response.choices[0].message.content
