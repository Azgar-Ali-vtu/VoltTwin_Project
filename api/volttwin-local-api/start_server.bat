@echo off
cd /d "%~dp0"
py -m pip install -r requirements.txt
if errorlevel 1 (
  echo Could not install packages. Check Python installation and internet connection.
  pause
  exit /b 1
)
py -m uvicorn server:app --host 127.0.0.1 --port 8000
pause
