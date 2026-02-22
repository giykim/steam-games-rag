import logging

from sqlalchemy import create_engine, text

from config import DATABASE_URL


class RetrievalService:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def retrieve(self, embedding: list[float], table: str, limit: int) -> list[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(
                text(f"""
                    SELECT app_id, name, content
                    FROM {table}
                    ORDER BY embedding <=> CAST(:embedding AS vector)
                    LIMIT :limit
                """),
                {
                    "embedding": str(embedding),
                    "limit": limit,
                }
            )

            rows = result.fetchall()
            logging.info(f"Retrieved {len(rows)} documents from {table}.")

            return [{"app_id": row.app_id, "name": row.name, "content": row.content} for row in rows]
