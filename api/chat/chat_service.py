from abc import ABC, abstractmethod
from collections import defaultdict

from openai import OpenAI

from api.models.chat_response import ChatResponse
from api.models.message import Message
from api.models.retrieval.retrieval_service import RetrievalService
from config import OPEN_AI_DESCRIPTION_TABLE, OPEN_AI_STATS_TABLE, OPENAI_API_KEY


class ChatService(ABC):
    MAX_HISTORY = 10
    EMBEDDING_MODEL = "text-embedding-3-small"
    SYSTEM_PROMPT = """You are a Steam game recommendation assistant.
        Start by asking what kind of game the user is looking for.
        After the user provides ANY preferences, immediately recommend 3-5 specific games from the context provided.
        For each game explain why it matches their preferences including price, genre, and playtime.
        You may ask one follow-up question after recommending, but always recommend first.
        Only recommend games that appear in the context. Do not make up games."""

    def __init__(self):
        self.embedding_client = OpenAI(api_key=OPENAI_API_KEY)
        self.retriever = RetrievalService()
        self.sessions: dict[str, list[dict]] = defaultdict(list)

    def chat(self, session_id: str, message: Message) -> ChatResponse:
        self.sessions[session_id].append({"role": "user", "content": message.content})

        embedding = self._embed_query(message.content)
        description_results = self.retriever.retrieve(embedding, OPEN_AI_DESCRIPTION_TABLE, 5)
        stats_results = self.retriever.retrieve(embedding, OPEN_AI_STATS_TABLE, 5)

        context = self._build_context(description_results, stats_results)
        response = self._generate_response(self.sessions[session_id], context)

        self.sessions[session_id].append({"role": "assistant", "content": response})

        return ChatResponse(message=Message(role="assistant", content=response))

    def _embed_query(self, query: str) -> list[float]:
        response = self.embedding_client.embeddings.create(input=query, model=self.EMBEDDING_MODEL)
        return response.data[0].embedding

    def _build_context(self, description_results: list[dict], stats_results: list[dict]) -> str:
        context_parts = ["Here are some relevant games:"]

        for desc, stats in zip(description_results, stats_results):
            context_parts.append(f"\n---\nGame: {desc['name']}\n{desc['content']}\n{stats['content']}")

        return "\n".join(context_parts)
    
    @abstractmethod
    def _generate_response(self, messages: list[Message], context: str) -> str:
        pass