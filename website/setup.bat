@echo off
echo ========================================
echo   Dipjo File Association Setup
echo ========================================
echo.
echo This will:
echo   1. Associate .dipjo files with Dipjo
echo   2. Set a custom icon for .dipjo files
echo   3. Allow double-click to run .dipjo files
echo.
echo Run this as Administrator!
echo.
pause
python "%~dp0setup_icon.py"
echo.
echo Done! You can now double-click .dipjo files.
pause
