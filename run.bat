@echo off
cd /d "%~dp0"
if exist "dist\SnakeGradient.exe" (
    start "" "dist\SnakeGradient.exe"
) else (
    python main.py
    if errorlevel 1 (
        echo.
        echo Game exited with error code %errorlevel%
        echo Press any key to close...
        pause >nul
    )
)
