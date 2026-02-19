from pipelines.etl.ingest import DataIngester
from pipelines.etl.preprocess import DataPreprocesser


class ETLService:
    def __init__(self):
        self.ingester = DataIngester()
        self.preprocesser = DataPreprocesser()

    def run(self):
        raw_df = self.ingester.load_kaggle_dataset()

        print(f"Loaded dataset with columns: {raw_df.columns.to_list()}")

        columns = ["name", "detailed_description"]
        preprocessed_df = self.preprocesser.select_columns(raw_df, columns)

        print(f"Preprocessed dataset: {preprocessed_df.columns.to_list()}")
