@echo off
chcp 65001 > nul
title EcoBot EcoBot56.py

echo Запуск EcoBot56.py...
python "EcoBot56.py"

echo.
echo Создание резервной копии сохранений...
set APPDATA_DIR=%APPDATA%\EcoBot
if not exist "%APPDATA_DIR%" mkdir "%APPDATA_DIR%" 2>nul
if exist "%APPDATA_DIR%" (
    if exist "C:\Users\stepa\OneDrive\Рабочий стол\EcoBot\saves\ecobot_save.json" (
        copy "C:\Users\stepa\OneDrive\Рабочий стол\EcoBot\saves\ecobot_save.json" "%APPDATA_DIR%\saves\" 2>nul
    )
    if exist "C:\Users\stepa\OneDrive\Рабочий стол\EcoBot\saves\settings.json" (
        copy "C:\Users\stepa\OneDrive\Рабочий стол\EcoBot\saves\settings.json" "%APPDATA_DIR%\saves\" 2>nul
    )
) else (
    echo Резервное копирование пропущено (нет прав доступа)
)

echo Готово.
pause
