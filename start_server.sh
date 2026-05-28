#!/bin/bash

echo "Starting FastAPI server in the background..."

# nohup과 &를 사용하여 백그라운드에서 실행하고, 로그를 server.log 파일에 저장합니다.
# 실행된 프로세스의 PID(프로세스 ID)를 server.pid 파일에 저장하여 나중에 종료할 때 사용합니다.
nohup ./.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
echo $! > server.pid

echo "Server is now running in the background."
echo "Logs are being written to server.log"
echo "Process ID saved to server.pid"
echo "To stop the server, run './stop_server.sh'."
