import json
import os

from openai import OpenAI

from config import PROCESSED_DATA_PATH


class DocumentEmbedder:
    EMBEDDING_MODEL = "text-embedding-3-small"
    EMBEDDINGS_PATH = PROCESSED_DATA_PATH / "embeddings.json"
    BATCH_SIZE = 100

    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def get_embeddings_documents(self, documents: list[dict]) -> str:
        if self.EMBEDDINGS_PATH.exists():
            embeddings_documents = self._load_embeddings()
        else:
            embeddings_documents = self._embed_documents(documents)
        
        return embeddings_documents

    def _embed_documents(self, documents: list[dict]) -> list[dict]:
        results = []

        for i in range(0, len(documents), self.BATCH_SIZE):
            batch = documents[i : i + self.BATCH_SIZE]

            texts = [doc["content"] for doc in batch]

            embeddings = self._embed_batch(texts)

            for doc, embedding in enumerate(batch, embeddings):
                results.append({**doc, "embedding": embedding})

            print(f"Embedded {min(i + self.BATCH_SIZE, len(documents))}/{len(documents)} documents.")

        return results

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            input = texts,
            model = self.EMBEDDING_MODEL,
        )

        return [item.embedding for item in response.data]
    
    def _load_embeddings(self) -> list[dict]:
        with open(PROCESSED_DATA_PATH, "r") as f:
            return json.load(f)
    
    def _save_embeddings(self, documents: list[dict]) -> None:
        with open(PROCESSED_DATA_PATH, "w") as f:
            json.dump(documents, f)
