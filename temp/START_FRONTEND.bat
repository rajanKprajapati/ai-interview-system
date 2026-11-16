@echo off
title AI Interview Frontend Server
cd /d "%~dp0frontend"

echo ===================================================
echo  Starting AI Interview Frontend (React 19 + Vite)
echo ===================================================
echo  Web Application: http://localhost:5173
echo ===================================================

where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm was not found in PATH!
    echo Please install Node.js (v18+) from https://nodejs.org/
    pause
    exit /b 1
)

if not exist node_modules (
    echo [INFO] node_modules not detected. Installing dependencies...
    call npm install
)

call npm run dev
pause
