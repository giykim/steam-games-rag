from pipelines.ingestion.ingest_service import IngestService


if __name__ == "__main__":
    service = IngestService()
    service.run()
