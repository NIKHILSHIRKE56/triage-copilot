@echo off
cd /d "%~dp0"

echo [1/3] Starting Docker containers (PostgreSQL + Ollama)...
docker compose up -d
timeout /t 5 /nobreak >nul

echo [2/3] Starting FastAPI Backend (Port 8000)...
start "Triage Copilot - FastAPI" cmd /k "set PYTHONPATH=. && .venv\Scripts\python.exe -m uvicorn app.main:app --port 8000"
timeout /t 3 /nobreak >nul

echo [3/3] Starting Streamlit UI (Port 8501)...
start "Triage Copilot - Streamlit UI" cmd /k ".venv\Scripts\python.exe -m streamlit run ui/app.py"

echo All services launched!
