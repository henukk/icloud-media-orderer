@echo off
REM Navigate to the project directory
cd /d %~dp0

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)

REM Create virtual environment if not exists
IF NOT EXIST venv (
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install required Python packages
pip install -r requirements.txt

REM Set environment variable for ExifTool (if needed)
set EXIFTOOL_PATH=%~dp0exiftool\exiftool.exe

REM Navigate to the src directory
cd src

REM Run the Streamlit application
streamlit run main.py

REM Deactivate the virtual environment after closing Streamlit
deactivate
pause
