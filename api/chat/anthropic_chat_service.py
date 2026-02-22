import logging

import anthropic

from api.chat.chat_service import ChatService
from api.models.message import Message
from config import ANTHROPIC_API_KEY


SYSTEM_PROMPT = """You are a Steam game recommendation assistant.
Start by asking what kind of game the user is looking for.
After the user provides ANY preferences, immediately recommend 3-5 specific games from the context provided.
For each game explain why it matches their preferences including price, genre, and playtime.
You may ask one follow-up question after recommending, but always recommend first.
Only recommend games that appear in the context. Do not make up games."""


class AnthropicChatService(ChatService):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        super().__init__()

    def _generate_response(self, messages: list[Message], context: str) -> str:
        anthropic_messages = [{"role": m.role, "content": m.content} for m in messages]

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT + "\n\nContext:\n" + context,
            messages=anthropic_messages,
        )

        logging.info("Generated chat response.")
        return response.content[0].text
