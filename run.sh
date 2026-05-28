#!/usr/bin/env bash
# TinyPet 터미널 실행형 (macOS / Linux)
# 의존성 자동 설치 후 백그라운드로 실행
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Python 확인
if ! command -v python3 >/dev/null 2>&1; then
    echo "[TinyPet] python3을(를) 찾을 수 없습니다."
    echo "  macOS: brew install python   (또는 https://www.python.org/downloads/)"
    echo "  Linux: 패키지 매니저로 설치 (예: sudo apt install python3 python3-pip python3-tk)"
    exit 1
fi

# tkinter 확인 (Linux는 별도 패키지일 수 있음)
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "[TinyPet] tkinter 가 없습니다."
    echo "  Linux (Debian/Ubuntu): sudo apt install python3-tk"
    echo "  Linux (Fedora):        sudo dnf install python3-tkinter"
    exit 1
fi

# pynput 확인 / 설치
if ! python3 -c "import pynput" 2>/dev/null; then
    echo "[TinyPet] pynput 설치 중..."
    if ! python3 -m pip install --user --quiet pynput; then
        echo "[TinyPet] pynput 설치 실패. 펫은 동작하지만 전역 입력 감지는 꺼집니다."
    fi
fi

# 백그라운드 실행
LOG="/tmp/tinypet.log"
nohup python3 -m tinypet > "$LOG" 2>&1 &
disown
echo "[TinyPet] 시작됨 (PID $!, 로그: $LOG)"

# macOS Accessibility 안내
if [ "$(uname)" = "Darwin" ]; then
    cat <<'EOF'

[macOS 안내]
pynput 의 전역 키/마우스 감지는 "접근성(Accessibility)" 권한이 필요합니다.
첫 실행 시 권한 요청이 뜨지 않으면:
  시스템 설정 → 개인정보 보호 및 보안 → 접근성
  → 사용 중인 터미널(또는 Python) 항목 체크
EOF
fi
