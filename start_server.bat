@echo off
echo Installing required Python packages...
pip install fastapi uvicorn passlib[argon2] argon2-cffi python-jose[cryptography] sqlalchemy

echo Starting FastAPI server...
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
