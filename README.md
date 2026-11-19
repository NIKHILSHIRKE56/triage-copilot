flowchart LR
    User(["L1/L2 Support Engineer"]) -->|"1. Paste Stack Trace / API Log"| UI["Streamlit Demo UI<br/>Port 8501"]

    subgraph AirGapped ["100% Air-Gapped / Zero-Cost Local Environment"]
        UI -->|"2. POST /api/v1/triage"| API["FastAPI Triage Engine<br/>Python 3.13 / Port 8000"]

        subgraph Docker ["Docker Compose Stack"]
            Ollama["Ollama Runtime - NVIDIA GPU<br/>Port 11434<br/>- nomic-embed-text<br/>- qwen2.5-coder:3b"]
            PG[("PostgreSQL 16 + pgvector<br/>Port 5432<br/>Telecom Runbooks")]
        end

        API -->|"3. Embed Log"| Ollama
        API -->|"4. Cosine Similarity Search"| PG
        PG -->|"5. Top-K Matched Runbooks"| API
        API -->|"6. RAG Prompt + Log"| Ollama
        Ollama -->|"7. Structured JSON RCA"| API
    end

    API -->|"8. Render Triage Dashboard"| Output["Output:<br/>- Severity P1/P2/P3<br/>- Technical RCA and Steps<br/>- Read-Only SQL Check<br/>- Executive Client Update"]
