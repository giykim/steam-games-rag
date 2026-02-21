from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from config import DATABASE_URL


class DatabaseService:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def save_embeddings(self, documents: list[dict], table: str) -> None:
        try:
            with self.engine.connect() as conn:
                for doc in documents:
                    conn.execute(
                        text(f"""
                            INSERT INTO {table} (app_id, name, content, embedding)
                            VALUES (:app_id, :name, :content, :embedding)
                            ON CONFLICT (app_id) DO NOTHING
                        """),
                        {
                            "app_id": doc["app_id"],
                            "name": doc["name"],
                            "content": doc["content"],
                            "embedding": str(doc["embedding"]),
                        }
                    )

                    conn.commit()
        except OperationalError as e:
            raise ConnectionError(f"Failed to connect to the database: {e}") from e