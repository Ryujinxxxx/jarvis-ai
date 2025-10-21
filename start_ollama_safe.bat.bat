@echo off
echo ===== Checking Ollama server status =====

:: Check if port 11434 is in use
set PORT_IN_USE=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :11434') do (
    set PORT_IN_USE=1
    set PID=%%a
)

if "%PORT_IN_USE%"=="1" (
    echo Port 11434 is in use by PID %PID%. Killing stuck process...
    taskkill /PID %PID% /F
) else (
    echo Port 11434 is free.
)

:: Optional: Kill other Ollama processes that may cause conflicts
for /f "tokens=2" %%b in ('tasklist ^| findstr Ollama') do (
    echo Killing leftover Ollama PID %%b
    taskkill /PID %%b /F
)

:: Optional: Reset TCP stack to clear TIME_WAIT
echo Resetting TCP/IP stack...
netsh int ip reset >nul
netsh winsock reset >nul

:: Start Ollama server
echo ===== Starting Ollama server =====
start "" ollama serve

echo ===== Done =====
pause
