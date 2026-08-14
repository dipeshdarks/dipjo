@echo off
title Dipjo
color 0A

echo.
echo  ███████╗██╗██████╗     ██╗██╗██╗
echo  ██╔════╝██║██╔══██╗    ██║██║██║
echo  █████╗  ██║██║  ██║    ██║██║██║
echo  ██╔══╝  ██║██║  ██║    ╚═╝╚═╝╚═╝
echo  ██║     ██║██████╔╝    ██╗██╗██╗
echo  ╚═╝     ╚═╝╚═════╝     ╚═╝╚═╝╚═╝
echo.

if "%~1"=="" (
    echo  Usage: run.bat ^<file.dipjo^>
    echo.
    pause
    exit /b 1
)

python "%~dp0lib\main.py" "%~1"
pause
