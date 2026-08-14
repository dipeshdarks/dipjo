@echo off
title Dipjo Programming Language
color 0A

echo.
echo  ███████╗██╗██████╗     ██╗██╗██╗
echo  ██╔════╝██║██╔══██╗    ██║██║██║
echo  █████╗  ██║██║  ██║    ██║██║██║
echo  ██╔══╝  ██║██║  ██║    ╚═╝╚═╝╚═╝
echo  ██║     ██║██████╔╝    ██╗██╗██╗
echo  ╚═╝     ╚═╝╚═════╝     ╚═╝╚═╝╚═╝
echo.
echo  Dipjo Programming Language v0.1.0
echo  ─────────────────────────────────
echo.

if "%~1"=="" (
    echo  Usage: run_dipjo.bat ^<file.dipjo^>
    echo.
    echo  Examples:
    echo    run_dipjo.bat hello.dipjo
    echo    run_dipjo.bat examples\fibonacci.dipjo
    echo.
    pause
    exit /b 1
)

if not exist "%~1" (
    echo  Error: File '%~1' not found.
    echo.
    pause
    exit /b 1
)

if not "%~x1"==".dipjo" (
    echo  Error: File '%~1' is not a .dipjo file.
    echo.
    pause
    exit /b 1
)

echo  Running: %~nx1
echo  ─────────────────────────────────
echo.

"C:\Python310\python.exe" "C:\Users\Lenovo\Downloads\dipjo-main\dipjo-main\lib\main.py" "%~1"

echo.
echo  ─────────────────────────────────
echo  Done.
pause
