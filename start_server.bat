@echo off
echo Starting FastAPI server in the background...

REM /B 옵션을 사용하여 새 창 없이 백그라운드에서 uvicorn 서버를 실행합니다.
start "CardGachaServer" /B .\.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000

echo.
echo Server is now running in the background.
echo You can close this window.
echo To stop the server, run 'stop_server.bat'.
echo.

REM 잠시 멈춰서 사용자가 메시지를 읽을 수 있게 합니다.
timeout /t 5 > nul
