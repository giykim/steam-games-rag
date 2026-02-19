from abc import ABC, abstractmethod
import json

from config import PROCESSED_DATA_PATH


class BaseEmbedder(ABC):
    def __init__(self):
        self.EMBEDDINGS_PATH = PROCESSED_DATA_PATH / self._get_embeddings_file()

    def get_embeddings_documents(self, documents: list[dict]) -> list[dict]:
        if self.EMBEDDINGS_PATH.exists():
            embeddings_documents = self._load_embeddings()
        else:
            embeddings_documents = self._embed_documents(documents)
        
        return embeddings_documents
    
    def _embed_documents(self, documents: list[dict]) -> list[dict]:
        results = []

        batch_size = self._get_batch_size()
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]

            texts = [doc["content"] for doc in batch]

            embeddings = self._embed_batch(texts)

            for doc, embedding in zip(batch, embeddings):
                results.append({**doc, "embedding": embedding})

            print(f"Embedded {min(i + batch_size, len(documents))}/{len(documents)} documents.")

        return results
    
    def _load_embeddings(self) -> list[dict]:
        with open(self.EMBEDDINGS_PATH, "r") as f:
            return json.load(f)
    
    def _save_embeddings(self, documents: list[dict]) -> None:
        with open(self.EMBEDDINGS_PATH, "w") as f:
            json.dump(documents, f)

    @abstractmethod
    def _get_embeddings_file(self) -> str:
        pass

    @abstractmethod
    def _get_batch_size(self) -> int:
        pass

    @abstractmethod
    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        pass