from pipelines.etl.embedding.embedder_factory import EmbedderFactory
from pipelines.etl.etl_service import ETLService


if __name__ == "__main__":
    embedder = EmbedderFactory.create("openai")

    service = ETLService(embedder)
    service.run()
