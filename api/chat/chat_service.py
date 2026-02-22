from abc import ABC, abstractmethod

from sentence_transformers import SentenceTransformer

from api.models.chat_response import ChatResponse
from api.models.message import Message
from api.models.retrieval.retrieval_service import RetrievalService


class ChatService(ABC):
    def __init__(self):
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
    
    @abstractmethod
    def _generate_response(self, messages: list[Message], context: str) -> str:
        pass