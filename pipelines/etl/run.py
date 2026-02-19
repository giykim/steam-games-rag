from dotenv import load_dotenv

from pipelines.etl.embedding.embedder_factory import EmbedderFactory
from pipelines.etl.etl_service import ETLService


if __name__ == "__main__":
    load_dotenv()

    embedder = EmbedderFactory.create("SentenceTransformer")

    service = ETLService(embedder)
    service.run()
