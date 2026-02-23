import logging
import os
import time

from openai import OpenAI, RateLimitError
import tiktoken

from pipelines.etl.embedding.base_embedder import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):
    BATCH_SIZE = 50
    EMBEDDING_MODEL = "text-embedding-3-small"
    INTER_BATCH_DELAY = 0.5
    MAX_TOKENS = 8192
    MAX_RETRIES = 15

    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            max_retries=self.MAX_RETRIES,
        )
        self.tokenizer = tiktoken.encoding_for_model(self.EMBEDDING_MODEL)

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
                time.sleep(self.INTER_BATCH_DELAY)
                return [item.embedding for item in response.data]
            except RateLimitError:
                if attempt == self.MAX_RETRIES - 1:
                    raise
                logging.warning(f"Rate limit hit, retrying in {delay:.1f}s (attempt {attempt + 1}/{self.MAX_RETRIES})...")
                time.sleep(delay)
                delay = min(delay * 2, 60.0)

    def _truncate(self, text: str) -> str:
        tokens = self.tokenizer.encode(text)
        if len(tokens) > self.MAX_TOKENS:
            tokens = tokens[:self.MAX_TOKENS]
            return self.tokenizer.decode(tokens)
        return text
