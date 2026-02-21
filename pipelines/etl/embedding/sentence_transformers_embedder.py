from sentence_transformers import SentenceTransformer

from pipelines.etl.embedding.base_embedder import BaseEmbedder


class SentenceTransformerEmbedder(BaseEmbedder):
    BATCH_SIZE = 100
    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        self.model = SentenceTransformer(self.MODEL_NAME)

        super().__init__()

    def _get_embeddings_file(self, embedding_type: str) -> str:
        return f"sentenceTransformer_{embedding_type}_embeddings.json"
    
    def _get_batch_size(self):
        return self.BATCH_SIZE

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()
