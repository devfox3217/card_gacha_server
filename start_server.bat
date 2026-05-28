@echo off
echo Starting FastAPI server in the background...

REM .venv 가상 환경이 없으면 생성
IF NOT EXIST ".venv" (
    echo Virtual environment '.venv' not found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate.bat

    echo Installing required packages...
    pip install fastapi uvicorn passlib[argon2] argon2-cffi python-jose[cryptography] sqlalchemy
) ELSE (
    echo Virtual environment '.venv' found.
    call .venv\Scripts\activate.bat
)

REM /B 옵션을 사용하여 새 창 없이 백그라운드에서 uvicorn 서버를 실행합니다.
start "CardGachaServer" /B python -m uvicorn main:app --host 0.0.0.0 --port 8000

echo.
echo Server is now running in the background.
echo You can close this window.
echo To stop the server, run 'stop_server.bat'.
echo.

REM 잠시 멈춰서 사용자가 메시지를 읽을 수 있게 합니다.
timeout /t 5 > nul
