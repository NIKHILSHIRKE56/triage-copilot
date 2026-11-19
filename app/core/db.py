import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS runbooks (
                    id SERIAL PRIMARY KEY,
                    ticket_id VARCHAR(50) UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    content TEXT NOT NULL,
                    sql_check TEXT,
                    embedding vector(768)
                );
            """)
        conn.commit()
    print("Database and pgvector schema initialized successfully.")


if __name__ == "__main__":
    init_db()
