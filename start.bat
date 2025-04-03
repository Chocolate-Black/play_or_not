@echo off

echo activate virtual environment...
call venv\Scripts\activate

echo Start WebUI...
python web.py
if %errorlevel% neq 0 (
    echo Fail to start WebUI
    pause
    exit /b 1
)

pause
