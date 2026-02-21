from pgvector.psycopg2 import register_vector
from psycopg2.extras import execute_values
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from config import DATABASE_URL


class DatabaseService:
    BATCH_SIZE = 1000

    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def save_embeddings(self, documents: list[dict], table: str) -> None:
        params = [
            (doc["app_id"], doc["name"], doc["content"], doc["embedding"])
            for doc in documents
        ]

        try:
            with self.engine.connect() as conn:
                raw_conn = conn.connection.dbapi_connection
                register_vector(raw_conn)
                with raw_conn.cursor() as cursor:
                    for i in tqdm(range(0, len(params), self.BATCH_SIZE), desc=f"Inserting into {table}"):
                        execute_values(
                            cursor,
                            f"""
                                INSERT INTO {table} (app_id, name, content, embedding)
                                VALUES %s
                                ON CONFLICT (app_id) DO NOTHING
                            """,
                            params[i : i + self.BATCH_SIZE],
                        )
                conn.commit()
        except OperationalError as e:
            raise ConnectionError(f"Failed to connect to the database: {e}") from e
