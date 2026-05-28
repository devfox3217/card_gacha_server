#!/bin/bash

echo "Starting FastAPI server in the background..."

# .venv 가상 환경이 없으면 python3를 사용하여 생성하고 활성화
if [ ! -d ".venv" ]; then
    echo "Virtual environment '.venv' not found. Creating one with python3..."
    python3 -m venv .venv
    source .venv/bin/activate

    echo "Installing required packages..."
    pip install fastapi uvicorn passlib[argon2] argon2-cffi python-jose[cryptography] sqlalchemy
else
    echo "Virtual environment '.venv' found."
    source .venv/bin/activate
fi

# 가상환경 내부의 python 실행 파일을 직접 사용하여 서버를 실행합니다.
# 이렇게 하면 시스템의 python 버전과 무관하게 안정적으로 동작합니다.
nohup ./.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
echo $! > server.pid

echo "Server is now running in the background."
echo "Logs are being written to server.log"
echo "Process ID saved to server.pid"
echo "To stop the server, run './stop_server.sh'."
