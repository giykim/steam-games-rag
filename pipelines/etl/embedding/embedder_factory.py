from pipelines.etl.embedding.base_embedder import BaseEmbedder
from pipelines.etl.embedding.openai_embedder import OpenAIEmbedder
from pipelines.etl.embedding.sentence_transformers_embedder import SentenceTransformerEmbedder


class EmbedderFactory:
    @staticmethod
    def create(provider: str) -> BaseEmbedder:
        provider = provider.lower()

        if provider == "openai":
            return OpenAIEmbedder()
        elif provider == "sentencetransformer":
            return SentenceTransformerEmbedder()
        else:
            raise ValueError("Unknown provider passed to EmbedderFactory.")