import pandas as pd


class DataPreprocesser:
    def __init__(self):
        pass

    def select_columns(self, raw_df: pd.DataFrame, columns: list) -> pd.DataFrame:
        df = raw_df.copy()

        df = df[columns]

        return df