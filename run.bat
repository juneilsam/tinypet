@echo off
REM TinyPet 터미널 실행형 - 의존성 자동 설치 후 백그라운드 실행
setlocal

where python >nul 2>nul
if errorlevel 1 (
    echo [TinyPet] Python을 찾을 수 없습니다.
    echo Python 3.8 이상 설치: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM pynput 확인 - 없으면 설치 시도
python -c "import pynput" 2>nul
if errorlevel 1 (
    echo [TinyPet] pynput 설치 중...
    python -m pip install --user --quiet pynput
    if errorlevel 1 (
        echo [TinyPet] pynput 설치 실패. 펫은 동작하지만 전역 입력 감지는 꺼집니다.
    )
)

REM pythonw 로 콘솔 없이 백그라운드 실행
start "" pythonw -m tinypet
endlocal
