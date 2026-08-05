@echo off
 title Build HS Service Management System v3.2 EXE
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed or not added to PATH.
    echo Install Python 3.11+ from python.org and tick "Add Python to PATH".
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install pyinstaller

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

python -m PyInstaller ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --name "HS_Service_Management_System_v3_2" ^
  --icon "assets\hs_sms_icon.ico" ^
  --add-data "README_CLIENT.txt;." ^
  --add-data "assets;assets" ^
  HS_Service_Management_System_v2.py

if exist dist\HS_Service_Management_System_v3_2.exe (
    echo.
    echo Build complete.
    echo Final EXE: dist\HS_Service_Management_System_v3_2.exe
    echo.
) else (
    echo.
    echo Build failed. Check the error above.
    echo.
)
pause
