@echo off
echo Stopping the background FastAPI server...

REM start 명령어의 제목을 기준으로 프로세스를 찾아 종료합니다.
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq CardGachaServer*"

echo.
echo Server has been stopped.
echo.

REM 잠시 멈춰서 사용자가 메시지를 읽을 수 있게 합니다.
pause
