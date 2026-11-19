# 📡 Air-Gapped Log & API Triage Copilot

A **100% open-source, zero-cost, air-gapped AI triage assistant** designed for enterprise telecom technical support teams (L1/L2/Lead). It ingests raw Java stack traces, REST API 4xx/5xx payloads, database deadlocks, and Linux kernel logs, retrieves matching historical runbooks via local vector search, and outputs both a **Technical RCA + Read-Only SQL Check** and a **Non-Technical Executive Update**.

---

## 🎯 Why Air-Gapped?
Enterprise telecom production logs contain sensitive subscriber PII (MSISDNs, ICCIDs) and proprietary carrier architecture. This system runs **100% on-premise with zero external LLM API calls** and **₹0 licensing cost**, making it safe to replicate in regulated production environments.

---

## 🏗️ System Architecture

```mermaid
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
```

---

## 🛠️ Tech Stack (100% Open-Source)
* **Local LLM Runtime:** Ollama with NVIDIA GPU passthrough (`qwen2.5-coder:3b` — right-sized for 4GB+ VRAM for 1–2s local inference)
* **Local Embeddings:** Ollama (`nomic-embed-text`, 768 dimensions)
* **Vector + Relational Database:** PostgreSQL 16 + `pgvector`
* **Backend API:** Python 3.13, FastAPI, Uvicorn, `psycopg`, `httpx`
* **Interactive Demo UI:** Streamlit
* **Containerization:** Docker Compose

---

## ✨ Key Features
* **Semantic Runbook Retrieval (RAG):** Converts incoming incident logs into 768-dim vectors and performs cosine similarity search against historical telecom runbooks (`DNO-1042`, `DNO-1189`, `DNO-1255`).
* **Dual-Audience Output:**
  * *For L1/L2 Engineers:* Severity classification (`P1`/`P2`/`P3`), root cause analysis, 3 concrete remediation steps, and a read-only PostgreSQL verification query.
  * *For Enterprise Stakeholders:* A concise, non-technical status update tailored to the affected carrier.
* **Built-In Telecom Presets:** One-click demo scenarios for **eSIM Provisioning 504 Timeout**, **Billing DB Deadlock (SQLState 40P01)**, and **MNP Port-In Validation Failure (HTTP 422)**.
* **One-Click Operations:** Includes `start_app.bat` and `stop_app.bat` for instant local launch and teardown.

---

## 📋 Agile Delivery (Scrum Documentation)
* [Project Charter](docs/agile/PROJECT_CHARTER.md)
* [Sprint 1: Infrastructure & GPU Ollama](docs/agile/SPRINT_1_BOARD.md)
* [Sprint 2: Telecom Knowledge Base & pgvector RAG](docs/agile/SPRINT_2_BOARD.md)
* [Sprint 3: FastAPI Triage Engine](docs/agile/SPRINT_3_BOARD.md)
* [Sprint 4: Interactive Demo UI & Release](docs/agile/SPRINT_4_BOARD.md)

---

## 🚀 Quickstart

### 1. Clone & Configure
```bash
git clone https://github.com/NIKHILSHIRKE56/triage-copilot.git
cd triage-copilot
cp .env.example .env
```

### 2. Start Containers & Pull Local Models (First-Time Only)
```bash
docker compose up -d
docker exec -it triage_ollama ollama pull qwen2.5-coder:3b
docker exec -it triage_ollama ollama pull nomic-embed-text
```

### 3. Install Dependencies & Ingest Runbooks (First-Time Only)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
\$env:PYTHONPATH="."
python app/core/db.py
python app/services/ingest.py
```

### 4. Launch the Application
* **Windows (One-Click):** Double-click `start_app.bat` (and `stop_app.bat` to shut down).
* **Manual:**
  ```powershell
  uvicorn app.main:app --port 8000
  streamlit run ui/app.py
  ```
