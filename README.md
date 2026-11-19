@'
# 📡 Air-Gapped Log & API Triage Copilot

A **100% open-source, zero-cost, air-gapped AI triage assistant** designed for enterprise telecom technical support teams (L1/L2/Lead). It ingests raw Java stack traces, REST API 4xx/5xx payloads, database deadlocks, and Linux kernel logs, retrieves matching historical runbooks via local vector search, and outputs both a **Technical RCA + Read-Only SQL Check** and a **Non-Technical Executive Update**.

---

## 🎯 Why Air-Gapped?
Enterprise telecom production logs contain sensitive subscriber PII (MSISDNs, ICCIDs) and proprietary carrier architecture. This system runs **100% on-premise with zero external LLM API calls** and **₹0 licensing cost**, making it safe to replicate in regulated production environments.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    User([L1/L2 Support Engineer]) -->|1. Paste Stack Trace / API Log| UI[Streamlit Demo UI<br/>Port 8501]

    subgraph AirGapped [100% Air-Gapped / Zero-Cost Local Environment]
        UI -->|2. POST /api/v1/triage| API[FastAPI Triage Engine<br/>Python 3.13 / Port 8000]

        subgraph Docker [Docker Compose Stack]
            Ollama[Ollama Runtime - NVIDIA GPU<br/>Port 11434<br/>• nomic-embed-text<br/>• qwen2.5-coder:3b]
            PG[(PostgreSQL 16 + pgvector<br/>Port 5432<br/>Telecom Runbooks)]
        end

        API -->|3. Embed Log| Ollama
        API -->|4. Cosine Similarity Search| PG
        PG -->|5. Top-K Matched Runbooks| API
        API -->|6. RAG Prompt + Log| Ollama
        Ollama -->|7. Structured JSON RCA| API
    end

    API -->|8. Render Triage Dashboard| Output[Output:<br/>• Severity P1/P2/P3<br/>• Technical RCA & Steps
