from pipelines.etl.ingester import DataIngester


class ETLService:
    def __init__(self):
        self.ingester = DataIngester()

    def run(self):
        dataset = self.ingester.load_kaggle_dataset()

        print(f"Loaded dataset: {dataset}")
