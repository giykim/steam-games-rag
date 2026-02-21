import pandas as pd


class DataPreprocesser:
    APP_ID_COLUMN = "appid"
    NAME_COLUMN = "name"

    def __init__(self):
        pass

    def build_documents(self, df: pd.DataFrame, columns_groups: list[list[str]]) -> list[dict]:
        documents = []

        for columns in columns_groups:
            if self.APP_ID_COLUMN not in columns or self.NAME_COLUMN not in columns:
                print(f"Columns {self.APP_ID_COLUMN} and {self.NAME_COLUMN} are required columns. Skipping creating documents for {columns}.")
                continue

            group_df = self._select_columns(df, columns)
            group_df = self._remove_na(group_df)

            for _, row in group_df.iterrows():
                documents.append({
                    "app_id": row[self.APP_ID_COLUMN],
                    "name": row[self.NAME_COLUMN],
                    "content": self._build_content(row),
                })

        return documents

    def _select_columns(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        df = df.copy()

        return df[columns]
    
    def _remove_na(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        return df.dropna()
    
    def _build_content(self, row: pd.Series) -> str:
        return "\n".join(
            f"{col.replace('_', '').title()}: {row[col]}"
            for col in row.index
            if not col == "name"
        )
