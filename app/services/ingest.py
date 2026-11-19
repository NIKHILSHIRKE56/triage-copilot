import json
import os
import httpx
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from app.core.db import get_connection

load_dotenv()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL")


def get_embedding(text: str) -> list[float]:
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=120.0,
    )
    response.raise_for_status()
    return response.json()["embedding"]


def ingest_runbooks(filepath: str = "data/runbooks/runbooks.json"):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        runbooks = json.load(f)

    with get_connection() as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            for rb in runbooks:
                text_to_embed = f"{rb['title']}\nCategory: {rb['category']}\n{rb['content']}"
                embedding = get_embedding(text_to_embed)

                cur.execute(
                    """
                    INSERT INTO runbooks (ticket_id, title, category, content, sql_check, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticket_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        category = EXCLUDED.category,
                        content = EXCLUDED.content,
                        sql_check = EXCLUDED.sql_check,
                        embedding = EXCLUDED.embedding;
                    """,
                    (
                        rb["ticket_id"],
                        rb["title"],
                        rb["category"],
                        rb["content"],
                        rb["sql_check"],
                        embedding,
                    ),
                )
                print(f"Indexed runbook: {rb['ticket_id']} - {rb['title']}")
        conn.commit()
    print("All runbooks ingested successfully.")


if __name__ == "__main__":
    ingest_runbooks()
