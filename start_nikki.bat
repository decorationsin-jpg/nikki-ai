@echo off
title Nikki - Autonomous Local AI Assistant
cls
echo =========================================================================
echo  🌸 NIKKI - YOUR AUTONOMOUS LOCAL AI ASSISTANT (ONE-CLICK LAUNCHER) 🌸
echo =========================================================================
echo.
echo Select how you want to launch Nikki:
echo.
echo   [1] Launch Nikki's Visual Web Face Dashboard (Browser GUI)
echo   [2] Launch Nikki Continuous Voice Conversation Mode
echo   [3] Run System Health & Security Diagnostic Audit
echo   [4] Start Interactive Terminal CLI Mode
echo   [5] Exit Launcher
echo.
set /p choice="Enter choice [1-5]: "

if "%choice%"=="1" (
    echo.
    echo Launching Nikki Visual Web Face Dashboard...
    python main.py --gui
    pause
)
if "%choice%"=="2" (
    echo.
    echo Launching Nikki Continuous Voice Mode...
    python main.py --voice
    pause
)
if "%choice%"=="3" (
    echo.
    echo Running Nikki System Health Check...
    python -c "from modules.health_checker import SystemHealthChecker; SystemHealthChecker().run_full_diagnostic()"
    pause
)
if "%choice%"=="4" (
    echo.
    echo Starting Nikki CLI...
    python main.py
    pause
)
if "%choice%"=="5" (
    exit
)
