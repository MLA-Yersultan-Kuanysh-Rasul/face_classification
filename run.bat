@echo off
echo ========================================
echo Starting Face Detector...
echo ========================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

if not exist "model\best_model.h5" (
    echo Error: Model file not found!
    echo Please ensure model/best_model.h5 exists.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Flask server...
echo.
echo ========================================
echo Application running at:
echo http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop
echo.

venv\Scripts\python.exe app.py
pause
