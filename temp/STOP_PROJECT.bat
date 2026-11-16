@echo off
title Stop AI Interview System
cd /d "%~dp0"

echo =====================================================================
echo             STOPPING AI INTERVIEW PREPARATION SYSTEM
echo =====================================================================
echo.

echo Stopping Backend on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Stopping Backend PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo Stopping Frontend on port 5173...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173 ^| findstr LISTENING') do (
    echo Stopping Frontend PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo [OK] AI Interview servers on ports 8000 and 5173 have been stopped.
echo =====================================================================
pause
