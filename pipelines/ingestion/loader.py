from config import KAGGLE_DATASET

import kagglehub


class DataLoader:
    def __init__(self):
        pass

    def download_kaggle_dataset(self):
        path = kagglehub.dataset_download(KAGGLE_DATASET)
        return path
