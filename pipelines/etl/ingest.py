import pandas as pd

import kagglehub

from config import RAW_DATA_PATH
from pipelines.etl.constants import CSV_FILE, KAGGLE_DATASET


class DataIngester:
    def __init__(self):
        pass

    def load_kaggle_dataset(self) -> pd.DataFrame:
        path = self._download_kaggle_dataset()

        raw_dataset = pd.read_csv(path / CSV_FILE)

        return raw_dataset

    def _download_kaggle_dataset(self) -> str:
        try:
            path = kagglehub.dataset_download(handle=KAGGLE_DATASET, output_dir=RAW_DATA_PATH)
            print(f"Downloaded kaggle dataset to {path}.")

            return path
        except Exception as e:
            raise RuntimeError(f"Failed to download Kaggle dataset '{KAGGLE_DATASET}': {e}") from e
