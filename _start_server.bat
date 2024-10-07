echo off
start cmd /k "venv\Scripts\activate.bat & uvicorn server.py.main:app --reload"
start chrome http://localhost:8000