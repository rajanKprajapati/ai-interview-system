@echo off
title AI Interview Preparation System Launcher
cd /d "%~dp0"

echo =====================================================================
echo           AI INTERVIEW PREPARATION & EVALUATION SYSTEM
echo         B.Tech Mini Project - CSE (Artificial Intelligence)
echo        Bansal Institute of Engineering & Technology, Lucknow
echo                   Student: Rajan Kumar Prajapati
echo =====================================================================
echo.

echo [1/3] Verifying environment prerequisites...

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in system PATH.
    echo Please install Python 3.10+ or check your PATH environment variable.
    pause
    exit /b 1
)
echo [OK] Python detected.

where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js / npm not found in system PATH.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js / npm detected.

echo.
echo [2/3] Launching Backend Server on port 8000...
start "AI Interview Backend" cmd /k ""%~dp0START_BACKEND.bat""

echo [3/3] Launching Frontend Application on port 5173...
start "AI Interview Frontend" cmd /k ""%~dp0START_FRONTEND.bat""

echo.
echo =====================================================================
echo  SERVICES LAUNCHED SUCCESSFULLY!
echo =====================================================================
echo.
echo  * Frontend Web App:  http://localhost:5173
echo  * Backend API:       http://127.0.0.1:8000
echo  * Interactive Docs:  http://127.0.0.1:8000/docs
echo  * Health Status:     http://127.0.0.1:8000/health
echo.
echo  To safely stop the application at any time, run: STOP_PROJECT.bat
echo =====================================================================
echo.
timeout /t 5 >nul
