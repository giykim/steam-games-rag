from pipelines.etl.embedding.openai_embedder import BaseEmbedder
from pipelines.etl.ingest import DataIngester
from pipelines.etl.preprocess import DataPreprocesser


class ETLService:
    def __init__(self, embedder: BaseEmbedder):
        self.ingester = DataIngester()
        self.preprocesser = DataPreprocesser()
        self.embedder = embedder

    def run(self):
        raw_df = self.ingester.get_kaggle_dataset()
        print(f"Loaded dataset with columns: {raw_df.columns.to_list()}")

        description_columns = ["name", "detailed_description", "genres", "tags"]
        stats_columns = ["name", "price", "metacritic_score", "average_playtime_forever"]
        documents = self.preprocesser.build_documents(raw_df, [description_columns, stats_columns])
        print(f"Created documents.")

        embeddings_documents = self.embedder.get_embeddings_documents(documents)
