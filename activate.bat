@echo off
echo Activating Bokehfolio virtual environment...

:: Check if venv exists, if not create ittttt
if not exist venv (
    echo Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate the virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

:: Show activated status and Python version
echo Virtual environment activated successfully!
python --version
echo.

:menu
cls
echo ===================================
echo        Bokehfolio Commands
echo ===================================
echo.
echo Choose a command to run:
echo 1. Run main.py
echo 2. Run dashboard.py
echo 3. Install requirements
echo 4. Update pip
echo 5. Exit
echo.
echo ===================================
set /p choice="Enter number (1-5): "

if "%choice%"=="1" (
    echo Running main.py...
    python main.py
    pause
    goto menu
)
if "%choice%"=="2" (
    echo Running dashboard.py...
    python dashboard.py
    pause
    goto menu
)
if "%choice%"=="3" (
    echo Installing requirements...
    pip install -r requirements.txt
    pause
    goto menu
)
if "%choice%"=="4" (
    echo Updating pip...
    python -m pip install --upgrade pip
    pause
    goto menu
)
if "%choice%"=="5" (
    echo Exiting...
    exit /b 0
)

echo Invalid choice. Please try again.
pause
goto menu