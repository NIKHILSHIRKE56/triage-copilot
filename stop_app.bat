@echo off
cd /d "%~dp0"
taskkill /FI "WINDOWTITLE eq Triage Copilot - FastAPI*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Triage Copilot - Streamlit UI*" /T /F >nul 2>&1
docker compose stop
echo All Triage Copilot services stopped.
pause
