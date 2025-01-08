@echo off
setlocal EnableDelayedExpansion

:: MarkoLabs Project Management Script
:: Created: 2025-01-08
:: This script provides an interactive menu system for managing the Python project

:menu
cls
echo ========================================
echo         MarkoLabs Manager
echo ========================================
echo.
echo   1. Run Dashboard
echo   2. Install Requirements
echo   3. Update pip
echo   4. Show Python Version
echo   5. Exit
echo.
echo ========================================

set /p choice="Enter your choice (1-5): "

:: Input validation
if "%choice%"=="" goto invalid
if %choice% gtr 5 goto invalid
if %choice% lss 1 goto invalid

:: Process the choice
if %choice%==1 goto run_dashboard
if %choice%==2 goto install_reqs
if %choice%==3 goto update_pip
if %choice%==4 goto show_version
if %choice%==5 goto end

:invalid
echo.
echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:run_dashboard
echo.
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo Error creating virtual environment.
        pause
        goto menu
    )
)
echo Running dashboard...
start "" http://localhost:8051
call venv\Scripts\activate.bat && python dashboard.py
if !errorlevel! neq 0 (
    echo Error running dashboard.
)
pause
goto menu

:install_reqs
echo.
if not exist "venv\Scripts\activate.bat" (
    echo Please create virtual environment first.
    pause
    goto menu
)
echo Installing requirements...
call venv\Scripts\activate.bat && pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo Error installing requirements.
) else (
    echo Requirements installed successfully.
)
pause
goto menu

:update_pip
echo.
if not exist "venv\Scripts\activate.bat" (
    echo Please create virtual environment first.
    pause
    goto menu
)
echo Updating pip...
call venv\Scripts\activate.bat && python -m pip install --upgrade pip
if !errorlevel! neq 0 (
    echo Error updating pip.
) else (
    echo Pip updated successfully.
)
pause
goto menu

:show_version
echo.
if not exist "venv\Scripts\activate.bat" (
    echo Please create virtual environment first.
    pause
    goto menu
)
echo Python version in virtual environment:
call venv\Scripts\activate.bat && python --version
pause
goto menu

:end
echo.
echo Thank you for using MarkoLabs Manager
timeout /t 2 >nul
exit
