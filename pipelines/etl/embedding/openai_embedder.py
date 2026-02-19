import os

from openai import OpenAI

from pipelines.etl.constants import EMBEDDINGS_FILE
from pipelines.etl.embedding.base_embedder import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):
    EMBEDDING_MODEL = "text-embedding-3-small"
    BATCH_SIZE = 100

    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        super().__init__()
        
    def _get_embeddings_file(self):
        return f"openAI_{EMBEDDINGS_FILE}"
    
    def _get_batch_size(self):
        return self.BATCH_SIZE

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            input = texts,
            model = self.EMBEDDING_MODEL,
        )

        return [item.embedding for item in response.data]
