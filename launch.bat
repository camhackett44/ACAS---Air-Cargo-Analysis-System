@echo off
title ACAS - Air Cargo Analysis System Launcher

:: Check for Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo 🔴 Python is not installed or not in PATH.
    echo.
    echo 🚨 Please install Python 3.x from: https://www.python.org/downloads/windows/
    echo ✅ IMPORTANT: During installation, check the box "Add Python to PATH"
    pause
    exit /b
)

:: Check for pip
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo 🔴 pip is not installed.
    echo You may need to reinstall Python with pip support or run:
    echo python -m ensurepip
    pause
    exit /b
)

:: Install required packages
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

:: Build database
echo 🏗️ Building local database from CSVs...
python reload_db.py

:: Launch dashboard
echo 🚀 Launching Streamlit dashboard...
python -m streamlit run dashboard.py

pause
