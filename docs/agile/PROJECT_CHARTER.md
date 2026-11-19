# Project Charter: Air-Gapped Log & API Triage Copilot

## 1. Business Problem
L1/L2 technical support teams spend 40-60% of Mean Time to Resolve (MTTR) manually parsing Java stack traces, correlating API 4xx/5xx payloads, and searching fragmented runbooks.

## 2. Solution & Enterprise Constraints
- **100% In-House / Air-Gapped:** Zero external LLM API calls to protect subscriber PII and carrier architecture.
- **Zero Licensing Cost:** Built strictly on open-source software (PostgreSQL/pgvector, Ollama, FastAPI, Streamlit).
- **Dual-Audience Output:** Generates both a Technical RCA (with DB verification queries) and a Non-Technical Executive Update.

## 3. Target KPIs (Production)
- Reduce initial incident triage time by 50%.
- Standardize L1-to-L2 escalation handoffs across 24x7 shifts.
