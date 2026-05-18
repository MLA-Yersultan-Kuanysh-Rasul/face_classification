@echo off
echo ========================================
echo Real vs Fake Face Detector - Setup
echo ========================================
echo.

echo [1/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To run the application:
echo   1. Run: run.bat
echo   2. Open: http://localhost:5000
echo.
pause
