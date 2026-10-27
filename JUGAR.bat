@echo off
title Geometry Dash - Pygame Edition
cd /d "%~dp0"
echo Iniciando Geometry Dash...
".venv\Scripts\python.exe" "02_juego_geometry_dash\main.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error al ejecutar el juego.
    pause
)
