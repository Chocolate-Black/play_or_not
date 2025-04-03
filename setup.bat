@echo off

echo create virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Fail to create virtual environment, please check your python
    pause
    exit /b 1
)

echo activate virtual environment...
call venv\Scripts\activate

echo install packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Fail to install packages
    pause
    exit /b 1
)

pause
