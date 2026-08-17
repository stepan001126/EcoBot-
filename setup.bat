 @echo off
chcp 65001 > nul
title EcoBot 55 - Установщик и Запуск

echo ========================================
echo       EcoBot 55 - Установка и Запуск
echo ========================================
echo.

:: Проверка наличия Python
echo [1/5] Проверка установки Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo.
    echo Пожалуйста, установите Python 3.14.3 или выше
    echo Скачать: https://www.python.org/downloads/
    echo.
    echo ИЛИ запустите установку через winget:
    echo winget install Python.Python.3.14
    echo.
    pause
    exit /b 1
)

:: Проверка версии Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo    Найдена версия: %PYTHON_VER%

:: Проверка минимальной версии (3.14.3)
for /f "tokens=1,2,3 delims=." %%a in ("%PYTHON_VER%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
    set PY_PATCH=%%c
)

if %PY_MAJOR% LSS 3 (
    echo ❌ Требуется Python 3.14.3 или выше!
    pause
    exit /b 1
)
if %PY_MAJOR% EQU 3 if %PY_MINOR% LSS 14 (
    echo ❌ Требуется Python 3.14.3 или выше!
    pause
    exit /b 1
)
if %PY_MAJOR% EQU 3 if %PY_MINOR% EQU 14 if %PY_PATCH% LSS 3 (
    echo ⚠️ Рекомендуется Python 3.14.3 (у вас %PYTHON_VER%)
)

echo ✅ Версия Python подходит
echo.

:: Обновление pip
echo [2/5] Обновление pip...
python -m pip install --upgrade pip --quiet
echo ✅ pip обновлён
echo.

:: Установка зависимостей
echo [3/5] Установка зависимостей...
echo.

:: Список зависимостей с описанием
echo Устанавливаемые пакеты:
echo   - pygame (игровой движок)
echo   - pygame.gfxdraw (графика)
echo   - tkinter (интерфейс) - встроен в Python
echo.

:: Проверка и установка pygame
echo Установка pygame...
pip install pygame --quiet
if errorlevel 1 (
    echo ❌ Ошибка установки pygame!
    echo Попытка установки с --no-cache-dir...
    pip install pygame --no-cache-dir --quiet
)
echo ✅ pygame установлен
echo.

:: Проверка установленных пакетов
echo [4/5] Проверка установленных пакетов...
echo.

:: Проверка pygame
python -c "import pygame" 2>nul
if errorlevel 1 (
    echo ❌ pygame не установлен!
    echo Установка pygame...
    pip install pygame --quiet
) else (
    echo ✅ pygame установлен
)

:: Проверка tkinter
python -c "import tkinter" 2>nul
if errorlevel 1 (
    echo ⚠️ tkinter не найден (обычно встроен в Python)
    echo Если игра не запустится, установите python3-tk
) else (
    echo ✅ tkinter установлен
)

echo.

:: Создание папок для сохранений
echo [5/5] Создание папок для сохранений...
if not exist "saves" mkdir "saves"
if not exist "%APPDATA%\EcoBot" mkdir "%APPDATA%\EcoBot" 2>nul
if not exist "%APPDATA%\EcoBot\saves" mkdir "%APPDATA%\EcoBot\saves" 2>nul
echo ✅ Папки созданы
echo.

:: Копирование резервных копий
echo Создание резервной копии сохранений...
if exist "saves\ecobot_save.json" (
    copy "saves\ecobot_save.json" "%APPDATA%\EcoBot\saves\" 2>nul
    echo ✅ ecobot_save.json скопирован
)
if exist "saves\settings.json" (
    copy "saves\settings.json" "%APPDATA%\EcoBot\saves\" 2>nul
    echo ✅ settings.json скопирован
)
echo.

:: Запуск игры
echo ========================================
echo       Запуск EcoBot 55...
echo ========================================
echo.
echo Нажмите любую клавишу для запуска игры...
pause > nul

python "EcoBot55.py"

:: Если игра закрылась с ошибкой
if errorlevel 1 (
    echo.
    echo ❌ Игра завершилась с ошибкой
    echo Проверьте установленные пакеты:
    echo   pip list
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo       Игра завершена
echo ========================================
echo.
pause