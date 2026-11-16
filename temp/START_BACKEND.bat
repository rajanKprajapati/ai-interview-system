@echo off
title AI Interview Backend Server
cd /d "%~dp0backend"

echo ===================================================
echo  Starting AI Interview Backend (FastAPI + Uvicorn)
echo ===================================================
echo  API Documentation (Swagger): http://127.0.0.1:8000/docs
echo  Health Check: http://127.0.0.1:8000/health
echo ===================================================

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in PATH!
    echo Please install Python 3.10+ or add it to your system PATH.
    pause
    exit /b 1
)

python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
