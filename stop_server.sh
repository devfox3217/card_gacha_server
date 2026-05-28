#!/bin/bash

echo "Stopping the background FastAPI server..."

# server.pid 파일이 존재하는지 확인
if [ -f server.pid ]; then
    # 파일에서 PID를 읽어옴
    PID=$(cat server.pid)

    # 해당 PID를 가진 프로세스를 종료
    kill $PID

    # PID 파일 삭제
    rm server.pid

    echo "Server with PID $PID has been stopped."
else
    echo "PID file (server.pid) not found. Is the server running?"
fi
