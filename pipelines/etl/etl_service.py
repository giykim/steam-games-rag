import logging

from pipelines.etl.constants import SENTENCE_TRANSFORMER_DESCRIPTION_TABLE, SENTENCE_TRANSFORMER_STATS_TABLE
from pipelines.etl.db.database_service import DatabaseService
from pipelines.etl.embedding.openai_embedder import BaseEmbedder
from pipelines.etl.ingestion.data_ingester import DataIngester
from pipelines.etl.preprocessing.data_preprocesser import DataPreprocesser


class ETLService:
    def __init__(self, embedder: BaseEmbedder):
        self.embedder = embedder

        self.db = DatabaseService()
        self.ingester = DataIngester()
        self.preprocesser = DataPreprocesser()

    def run(self):
        raw_df = self.ingester.get_kaggle_dataset()
        logging.info(f"Loaded dataset with columns: {raw_df.columns.to_list()}")

        description_columns = ["appid", "name", "detailed_description", "genres", "tags"]
        description_documents = self.preprocesser.build_documents(raw_df, description_columns)
        logging.info("Created description documents.")
    
        stats_columns = ["appid", "name", "price", "metacritic_score", "average_playtime_forever"]
        stats_documents = self.preprocesser.build_documents(raw_df, stats_columns)
        logging.info("Created stats documents.")

        embedded_description = self.embedder.get_embeddings_documents(description_documents, "description")
        embedded_stats = self.embedder.get_embeddings_documents(stats_documents, "stats")
        logging.info("Retrieved embeddings.")

        self.db.save_embeddings(embedded_description, SENTENCE_TRANSFORMER_DESCRIPTION_TABLE)
        self.db.save_embeddings(embedded_stats, SENTENCE_TRANSFORMER_STATS_TABLE)
        logging.info("Saved embeddings to database.")

        logging.info("Finished running ETL service.")
