import logging

from openai import OpenAI

from api.chat.chat_service import ChatService
from api.models.message import Message
from config import OPENAI_API_KEY


SYSTEM_PROMPT = """You are a Steam game recommendation assistant.
Your goal is to recommend games based on the user's preferences.
Start by asking what kind of game they are looking for.
Follow up with questions about price range, genre, multiplayer preference, and playtime.
When recommending games, explain why each game matches their preferences.
Base your recommendations only on the context provided to you.
If you don't have enough information to make a recommendation, ask for more details."""


class OpenAIChatService(ChatService):
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        super().__init__()

    def _generate_response(self, messages: list[Message], context: str) -> str:
        openai_messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\nContext:\n" + context}]
        openai_messages += [{"role": m.role, "content": m.content} for m in messages]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=openai_messages,
        )

        logging.info("Generated chat response.")
        return response.choices[0].message.content
