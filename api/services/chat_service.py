import logging

from openai import OpenAI
from sentence_transformers import SentenceTransformer

from api.services.retrieval_service import RetrievalService
from api.models.chat_response import ChatResponse
from api.models.message import Message
from config import OPENAI_API_KEY


SYSTEM_PROMPT = """You are a Steam game recommendation assistant.
Your goal is to recommend games based on the user's preferences.
Start by asking what kind of game they are looking for.
Follow up with questions about price range, genre, multiplayer preference, and playtime.
When recommending games, explain why each game matches their preferences.
Base your recommendations only on the context provided to you.
If you don't have enough information to make a recommendation, ask for more details."""


class ChatService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.retriever = RetrievalService()

    def chat(self, messages: list[Message]) -> ChatResponse:
        query = messages[-1].content

        embedding = self._embed_query(query)
        description_results = self.retriever.retrieve(embedding, "description_embeddings_st", 5)
        stats_results = self.retriever.retrieve(embedding, "stats_embeddings_st", 5)

        context = self._build_context(description_results, stats_results)
        response = self._generate_response(messages, context)

        return ChatResponse(message=Message(role="assistant", content=response))

    def _embed_query(self, query: str) -> list[float]:
        return self.model.encode(query).tolist()

    def _build_context(self, description_results: list[dict], stats_results: list[dict]) -> str:
        context_parts = ["Here are some relevant games:"]

        for desc, stats in zip(description_results, stats_results):
            context_parts.append(f"\n---\nGame: {desc['name']}\n{desc['content']}\n{stats['content']}")

        return "\n".join(context_parts)

    def _generate_response(self, messages: list[Message], context: str) -> str:
        openai_messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\nContext:\n" + context}]
        openai_messages += [{"role": m.role, "content": m.content} for m in messages]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=openai_messages,
        )

        logging.info("Generated chat response.")
        return response.choices[0].message.content
