@echo off
REM TinyPet 단순 실행형 빌드 (PyInstaller -> dist\TinyPet.exe)
setlocal

where python >nul 2>nul
if errorlevel 1 (
    echo [TinyPet] Python을 찾을 수 없습니다.
    pause
    exit /b 1
)

echo [TinyPet] 의존성 + PyInstaller 확인...
python -m pip install --user --quiet pynput pyinstaller
if errorlevel 1 (
    echo [TinyPet] 의존성 설치 실패
    pause
    exit /b 1
)

echo [TinyPet] 빌드 시작...
python -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name TinyPet ^
    --hidden-import pynput.keyboard._win32 ^
    --hidden-import pynput.mouse._win32 ^
    tinypet\pet.py

if errorlevel 1 (
    echo [TinyPet] 빌드 실패
    pause
    exit /b 1
)

echo.
echo [TinyPet] 완료! 결과물: dist\TinyPet.exe
echo.
pause
endlocal
