# Sprint 2: Telecom Knowledge Base & Local RAG

## Sprint Goal
Set up the Python environment, initialize PostgreSQL with pgvector, author realistic DNO Cloud / Nomad eSIM runbooks, and build the local vector ingestion pipeline using Ollama (`nomic-embed-text`).

## Tasks
- [ ] T2.1: Set up Python virtual environment and install dependencies
- [ ] T2.2: Configure `.env` for local Postgres and Ollama
- [ ] T2.3: Create `pgvector` schema (`runbooks` table with 768-dim embeddings)
- [ ] T2.4: Author 3 telecom runbooks (eSIM 504, Billing Deadlock, MNP 422)
- [ ] T2.5: Build and execute `ingest.py` to embed and store runbooks
- [ ] T2.6: Verify semantic similarity search against `pgvector`
