@echo off
cls
echo ======================================================
echo      Rclone Backup Script Installer
echo ======================================================
echo.
echo This script will set up the necessary folders and
echo Python environment for your backup system.
echo.
pause
echo.

:: --- Step 1: Check for Python ---
echo [1/5] Checking for Python installation...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not found in your system's PATH.
    echo Please install Python and make sure it's added to your PATH.
    echo https://www.python.org/downloads/
    pause
    exit /b
)
echo      Python found!
echo.

:: --- Step 2: Create Directory Structure ---
echo [2/5] Creating folder structure...
if not exist "C:\rclone" mkdir "C:\rclone"

:: Check if the scripts folder exists. If so, remove it for a clean install.
if exist "C:\rclone\scripts" (
    echo      Existing scripts folder found. Removing for clean installation...
    rmdir /s /q "C:\rclone\scripts"
)

:: Create the new scripts folder
mkdir "C:\rclone\scripts"
echo      Folders created at C:\rclone\scripts
echo.

:: --- Step 3: Move Project Files ---
echo [3/5] Moving project files...
:: %~dp0 is a special variable that gets the directory of this setup.bat file
set "SOURCE_DIR=%~dp0"
set "DEST_DIR=C:\rclone\scripts"

:: List of files to move
set "FILES_TO_MOVE=backup.py config.json notify.py utils.py"

for %%F in (%FILES_TO_MOVE%) do (
    if exist "%SOURCE_DIR%\%%F" (
        echo      Moving %%F...
        move "%SOURCE_DIR%\%%F" "%DEST_DIR%\" >nul
    ) else (
        echo      WARNING: %%F not found, skipping.
    )
)
echo.

:: --- Step 4: Create and Prepare Python Virtual Environment ---
echo [4/5] Creating Python virtual environment and installing modules...
cd /d "%DEST_DIR%"
python -m venv venv >nul
echo      Virtual environment created.
echo      Installing 'requests' library...
call "%DEST_DIR%\venv\Scripts\activate.bat"
pip install requests >nul
call "%DEST_DIR%\venv\Scripts\deactivate.bat"
echo      'requests' installed successfully.
echo.

:: --- Step 5: Create the Launcher Batch File ---
echo [5/5] Creating the launcher script (run_backup.bat)...
(
    echo @"%DEST_DIR%\venv\Scripts\python.exe" "%DEST_DIR%\backup.py"
) > "%DEST_DIR%\run_backup.bat"
echo      Launcher created successfully.
echo.


:: --- Final Instructions ---
echo ======================================================
echo           SETUP COMPLETE!
echo ======================================================
echo.
echo Your backup system is now installed in C:\rclone\scripts
echo.
echo --- NEXT STEPS ---
echo 1. Edit the config.json file with your folder paths.
echo 2. Edit the notify.py file with your Telegram Bot Token and Chat ID.
echo 3. Set up Windows Task Scheduler to run the new
echo    'run_backup.bat' file located in C:\rclone\scripts
echo.
echo This window will close now.
pause
exit
