#!/usr/bin/env bash
# TinyPet macOS .app 번들 빌드 (PyInstaller -> dist/TinyPet.app)
# Linux 도 동일 스크립트로 단일 실행파일 dist/TinyPet 가 만들어짐
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
    echo "[TinyPet] python3을(를) 찾을 수 없습니다."
    exit 1
fi

echo "[TinyPet] 의존성 + PyInstaller 설치..."
python3 -m pip install --user --quiet pynput pyinstaller

echo "[TinyPet] 빌드 시작..."
EXTRA_FLAGS=()
if [ "$(uname)" = "Darwin" ]; then
    EXTRA_FLAGS+=(--osx-bundle-identifier "com.juneilsam.tinypet")
    EXTRA_FLAGS+=(--hidden-import pynput.keyboard._darwin)
    EXTRA_FLAGS+=(--hidden-import pynput.mouse._darwin)
else
    EXTRA_FLAGS+=(--hidden-import pynput.keyboard._xorg)
    EXTRA_FLAGS+=(--hidden-import pynput.mouse._xorg)
fi

python3 -m PyInstaller --noconfirm --clean --onefile --windowed \
    --name TinyPet \
    "${EXTRA_FLAGS[@]}" \
    tinypet/pet.py

echo
if [ "$(uname)" = "Darwin" ]; then
    echo "[TinyPet] 완료! dist/TinyPet.app"
    echo "  열기: open dist/TinyPet.app"
else
    echo "[TinyPet] 완료! dist/TinyPet"
    echo "  실행: ./dist/TinyPet"
fi
