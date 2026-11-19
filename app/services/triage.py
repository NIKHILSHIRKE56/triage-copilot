import json
import os
import httpx
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from app.core.db import get_connection
from app.services.ingest import get_embedding

load_dotenv()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL")


def search_runbooks(query_text: str, top_k: int = 2) -> list[dict]:
    query_embedding = get_embedding(query_text)
    with get_connection() as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ticket_id, title, category, content, sql_check,
                       ROUND((1 - (embedding <=> %s::vector))::numeric, 4) AS similarity
                FROM runbooks
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """,
                (query_embedding, query_embedding, top_k),
            )
            rows = cur.fetchall()

    return [
        {
            "ticket_id": r[0],
            "title": r[1],
            "category": r[2],
            "content": r[3],
            "sql_check": r[4],
            "similarity": float(r[5]),
        }
        for r in rows
    ]


def analyze_incident(incident_log: str, customer_name: str = "Enterprise Carrier") -> dict:
    matched_runbooks = search_runbooks(incident_log, top_k=2)
    context_text = "\n\n".join(
        [
            f"[{rb['ticket_id']}] {rb['title']} (Match: {rb['similarity']})\n"
            f"Details: {rb['content']}\n"
            f"SQL Check: {rb['sql_check']}"
            for rb in matched_runbooks
        ]
    )

    prompt = f"""You are a Senior Technical Support Lead for a cloud-native telecom BSS platform (DNO Cloud / Nomad eSIM).
Analyze the incoming production incident log using the retrieved historical runbooks below.

--- RETRIEVED RUNBOOKS ---
{context_text}

--- INCOMING INCIDENT LOG ---
Customer: {customer_name}
Log/Payload:
{incident_log}

Respond ONLY with a valid JSON object using these exact keys:
- "severity": "P1", "P2", or "P3"
- "matched_ticket_id": the most relevant ticket_id from the runbooks (or "NEW")
- "technical_rca": concise root cause explanation referencing the stack trace/API error
- "next_steps": array of 3 concrete debugging/remediation steps for an L1/L2 engineer
- "sql_verification": the exact read-only PostgreSQL query to verify impact
- "executive_update": a 2-3 sentence non-technical status update suitable for {customer_name} leadership
"""

    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "format": "json",
            "stream": False,
        },
        timeout=120.0,
    )
    response.raise_for_status()
    raw_output = response.json()["response"]

    return {
        "analysis": json.loads(raw_output),
        "retrieved_runbooks": matched_runbooks,
    }
