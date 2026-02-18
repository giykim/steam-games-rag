from loader import DataLoader


class IngestService:
    def __init__(self):
        self.data_loader = DataLoader()

    def run(self):
        path = self.data_loader.download_kaggle_dataset()

        print(path)