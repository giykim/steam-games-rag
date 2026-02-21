import os

from openai import OpenAI

from pipelines.etl.embedding.base_embedder import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):
    BATCH_SIZE = 500
    EMBEDDING_MODEL = "text-embedding-3-small"

    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        super().__init__()
        
    def _get_embeddings_file(self, embedding_type: str) -> str:
        return f"openAI_{embedding_type}_embeddings.json"
    
    def _get_batch_size(self):
        return self.BATCH_SIZE

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            input = texts,
            model = self.EMBEDDING_MODEL,
        )

        return [item.embedding for item in response.data]
