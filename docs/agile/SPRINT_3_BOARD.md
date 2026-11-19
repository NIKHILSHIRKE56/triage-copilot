# Sprint 3: FastAPI Triage Engine

## Sprint Goal
Build the core FastAPI backend that embeds incoming Java stack traces / API errors, retrieves matching telecom runbooks from pgvector, and generates structured Technical RCA + Executive Updates via local Ollama.

## Tasks
- [ ] T3.1: Build pp/services/triage.py (pgvector cosine search + Ollama JSON prompt)
- [ ] T3.2: Build pp/main.py with /health and POST /api/v1/triage
- [ ] T3.3: Launch Uvicorn server and verify Swagger UI (/docs)
- [ ] T3.4: Smoke-test /api/v1/triage with a live Java stack trace
