from abc import ABC, abstractmethod
import json
from tqdm import tqdm

from config import PROCESSED_DATA_PATH


class BaseEmbedder(ABC):
    def get_embeddings_documents(self, documents: list[dict], embedding_type: str) -> list[dict]:
        path = PROCESSED_DATA_PATH / self._get_embeddings_file(embedding_type)
        if path.exists():
            embeddings_documents = self._load_embeddings(path)
        else:
            embeddings_documents = self._embed_documents(documents, path)

        return embeddings_documents

    def _embed_documents(self, documents: list[dict], path) -> list[dict]:
        results = []

        batch_size = self._get_batch_size()
        batches = range(0, len(documents), batch_size)
        for i in tqdm(batches, desc="Embedding", unit="batch"):
            batch = documents[i : i + batch_size]

            texts = [doc["content"] for doc in batch]

            embeddings = self._embed_batch(texts)

            for doc, embedding in zip(batch, embeddings):
                results.append({**doc, "embedding": embedding})

        self._save_embeddings(results, path)

        return results

    def _load_embeddings(self, path) -> list[dict]:
        with open(path, "r") as f:
            return json.load(f)

    def _save_embeddings(self, documents: list[dict], path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(documents, f)

    @abstractmethod
    def _get_embeddings_file(self, embedding_type: str) -> str:
        pass

    @abstractmethod
    def _get_batch_size(self) -> int:
        pass

    @abstractmethod
    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        pass