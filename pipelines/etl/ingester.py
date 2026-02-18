import pandas as pd

import kagglehub

from config import RAW_DATA_PATH
from pipelines.etl.constants import CSV_FILE, KAGGLE_DATASET


class DataIngester:
    def __init__(self):
        pass

    def load_kaggle_dataset(self):
        path = self._download_kaggle_dataset()

        raw_dataset = pd.read_csv(path / CSV_FILE)

        return raw_dataset

    def _download_kaggle_dataset(self):
        path = kagglehub.dataset_download(handle=KAGGLE_DATASET, output_dir=RAW_DATA_PATH)

        print(f"Downloaded kaggle dataset at {path}.")

        return path
