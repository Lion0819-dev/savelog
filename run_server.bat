@echo off
chcp 65001 > nul

REM ============================
REM 仮想環境を有効化
REM ============================
call venv\Scripts\activate

REM ============================
REM PCのIPv4アドレスを取得
REM ============================
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do (
    set IP=%%a
    goto :found
)

:found
set IP=%IP: =%

echo.
echo ============================
echo  SaveLog サーバ起動中
echo ============================
echo  iPhone用アクセスURL:
echo  http://%IP%:8000
echo ============================
echo.

REM ============================
REM FastAPI 起動（外部接続可）
REM ============================
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
