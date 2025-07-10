@echo off
REM Start AS-FAQ-RAG (Windows batch)

setlocal ENABLEDELAYEDEXPANSION

REM Default: auto update disabled
set ENABLE_AUTO_UPDATE=0
set PORT=8000
set NEXT_IS_PORT=0

REM Check arguments
for %%A in (%*) do (
    if "%%A"=="--auto-update" set ENABLE_AUTO_UPDATE=1
    
    REM Check for --port followed by value
    if "!NEXT_IS_PORT!"=="1" (
        set PORT=%%A
        set NEXT_IS_PORT=0
    ) else (
        if "%%A"=="--port" set NEXT_IS_PORT=1
        
        REM Check for --port=value format
        set arg=%%A
        set prefix=!arg:~0,7!
        if "!prefix!"=="--port=" set PORT=!arg:~7!
    )
)

REM If no argument, check environment variable
if "%ENABLE_AUTO_UPDATE%"=="0" if "%ENABLE_AUTO_UPDATE_ENV%"=="1" set ENABLE_AUTO_UPDATE=1

if "%ENABLE_AUTO_UPDATE%"=="1" (
    echo Auto update enabled
    start /b python auto_update.py
) else (
    echo Auto update disabled
)

REM Start API service in foreground
uvicorn api:app --host 0.0.0.0 --port %PORT% 