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
        print(f"Loaded dataset with columns: {raw_df.columns.to_list()}")

        description_columns = ["appid", "name", "detailed_description", "genres", "tags"]
        stats_columns = ["appid", "name", "price", "metacritic_score", "average_playtime_forever"]
        documents = self.preprocesser.build_documents(raw_df, [description_columns, stats_columns])
        print(f"Created documents.")

        embeddings_documents = self.embedder.get_embeddings_documents(documents)
        print(f"Retrieved embeddings.")

        self.db.save_embeddings(embeddings_documents)
        print("Saved embeddings to database.")
