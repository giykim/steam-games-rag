import kagglehub

from config import RAW_DATA_PATH
from pipelines.ingestion.constants import KAGGLE_DATASET


class DataLoader:
    def __init__(self):
        pass

    def download_kaggle_dataset(self):
        path = kagglehub.dataset_download(handle=KAGGLE_DATASET, output_dir=RAW_DATA_PATH)

        return path
