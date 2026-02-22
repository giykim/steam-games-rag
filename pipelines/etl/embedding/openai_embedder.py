import logging
import os
import time

from openai import OpenAI, RateLimitError

from pipelines.etl.embedding.base_embedder import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):
    BATCH_SIZE = 50
    EMBEDDING_MODEL = "text-embedding-3-small"
    MAX_TOKENS = 8192
    MAX_RETRIES = 8

    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            max_retries=self.MAX_RETRIES,
        )

        super().__init__()

    def _get_embeddings_file(self, embedding_type: str) -> str:
        return f"openAI_{embedding_type}_embeddings.json"

    def _get_batch_size(self):
        return self.BATCH_SIZE

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        truncated = [self._truncate(t) for t in texts]

        delay = 1.0
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.client.embeddings.create(
                    input=truncated,
                    model=self.EMBEDDING_MODEL,
                )
                return [item.embedding for item in response.data]
            except RateLimitError:
                if attempt == self.MAX_RETRIES - 1:
                    raise
                logging.warning(f"Rate limit hit, retrying in {delay:.1f}s (attempt {attempt + 1}/{self.MAX_RETRIES})...")
                time.sleep(delay)
                delay = min(delay * 2, 60.0)

    def _truncate(self, text: str) -> str:
        return text[:self.MAX_TOKENS * 4]
