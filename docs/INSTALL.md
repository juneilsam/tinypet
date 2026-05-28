**한국어** · [English](INSTALL.en.md)

# 설치 가이드

세 가지 배포 방식이 있습니다. 자기 환경에 맞는 걸 고르세요.

| 방식 | 대상 | Python 필요 | 절차 |
|---|---|---|---|
| **A. 단순 실행형** | 일반 사용자 | 없음 | exe 다운로드 → 더블클릭 |
| **B. 터미널 설치형** | 파이썬 사용자 | 3.8+ | `pip install` 후 `tinypet` 명령 |
| **C. 터미널 실행형** | 개발자 / 로컬 실행 | 3.8+ | clone 후 `run.bat` |

---

## A. 단순 실행형 (Click-to-Run)

**플랫폼**: Windows / macOS  
**Python 설치**: 필요 없음

### Windows

1. [Releases 페이지](https://github.com/juneilsam/tinypet/releases) 이동
2. 최신 버전의 `TinyPet.exe` 다운로드
3. 원하는 폴더에 저장 → 더블클릭

화면 우상단에 펫이 자는 모습 `( ˘ㅅ˘ )zzZ` 으로 떠 있으면 성공.

**Windows SmartScreen 경고가 뜨면**: 서명되지 않은 exe라 처음 실행 시 "Windows의 PC 보호" 경고가 떠요. "추가 정보" → "실행" 클릭.

**자동 시작 등록**:
1. `Win+R` → `shell:startup` 입력 → Enter
2. 열린 폴더에 `TinyPet.exe` **바로가기**를 복사 (원본 파일 아님)

**제거**: exe 파일 삭제. 설정 파일도 지우려면:
```cmd
del %USERPROFILE%\.tinypet.json
```

### macOS

1. [Releases 페이지](https://github.com/juneilsam/tinypet/releases) 에서 `TinyPet-macos.zip` 다운로드
2. 압축 풀기 → `TinyPet.app` 더블클릭

**Gatekeeper 경고가 뜨면**: 서명/공증 안 된 앱이라 처음엔 차단됩니다.
- 우클릭 → **열기** → 다이얼로그에서 **열기** 한 번 더
- 또는 시스템 설정 → 개인정보 보호 및 보안 → "차단됨" 알림 옆 **열기 허용**

**접근성(Accessibility) 권한** (전역 키/마우스 감지에 필요):
1. 처음 실행 시 시스템이 권한 요청 다이얼로그를 띄움 → 허용
2. 안 뜨면: 시스템 설정 → 개인정보 보호 및 보안 → 접근성 → `TinyPet` 토글 켜기

권한 안 주면 펫 클릭 / 잠금-절전 감지 / 시간 기반 졸음만 동작 (외부 키·클릭으로 깨우기 안 됨).

**자동 시작 등록**: 시스템 설정 → 일반 → 로그인 항목 → `+` → `TinyPet.app` 선택.

**제거**: 앱 삭제 + 설정 파일:
```bash
rm ~/.tinypet.json
```

### Linux

빌드된 바이너리는 배포 안 함 (배포판 다양성 때문). **B** 또는 **C** 방법 사용.

---

## B. 터미널 설치형 (pip install)

**플랫폼**: Windows / macOS / Linux  
**필요**: Python 3.8 이상

Linux는 `python3-tk` 별도 설치 필요:
- Debian/Ubuntu: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch: `sudo pacman -S tk`

### Python 확인

```bash
python --version
```

3.8 미만이면 https://www.python.org/downloads/ 에서 설치.

### 설치

GitHub에서 직접:
```bash
pip install git+https://github.com/juneilsam/tinypet.git
```

### 실행

```bash
tinypet
```

또는:
```bash
python -m tinypet
```

콘솔 창 없이 백그라운드 실행:
```bash
pythonw -m tinypet
```

### 업데이트

```bash
pip install -U git+https://github.com/juneilsam/tinypet.git
```

### 제거

```bash
pip uninstall tinypet
```

---

## C. 터미널 실행형 (Clone & Run)

**플랫폼**: Windows 권장  
**필요**: Python 3.8+, git

### 1) 클론

```bash
git clone https://github.com/juneilsam/tinypet.git
cd tinypet
```

### 2-A) 헬퍼 스크립트 (추천)

Windows:
```cmd
run.bat
```

macOS / Linux:
```bash
./run.sh
```

하는 일 (공통):
- Python (+ Linux는 tkinter) 존재 확인
- `pynput` 없으면 자동 설치
- 콘솔 없이 백그라운드 실행 (`pythonw -m tinypet` / `nohup ... &`)

### 2-B) 수동 실행

```bash
pip install -r requirements.txt
python -m tinypet      # Windows
python3 -m tinypet     # macOS / Linux
```

콘솔/터미널 없이:
- Windows: `pythonw -m tinypet`
- macOS / Linux: `nohup python3 -m tinypet > /tmp/tinypet.log 2>&1 &`

개발용 (코드 수정하면서 즉시 반영):
```bash
pip install -e .
tinypet
```

---

## 자기 실행파일 빌드 (선택)

리포지토리 받은 뒤:

| 플랫폼 | 명령 | 결과물 |
|---|---|---|
| Windows | `build_exe.bat` | `dist\TinyPet.exe` |
| macOS | `./build_app.sh` | `dist/TinyPet.app` |
| Linux | `./build_app.sh` | `dist/TinyPet` (단일 ELF 바이너리) |

대략 30~40MB. PyInstaller `--onefile` 기반.

---

## 트러블슈팅

### "Python을 찾을 수 없습니다"
Python 미설치 또는 PATH에 없음. https://www.python.org/downloads/ 에서 설치 시 "Add Python to PATH" 체크.

### "pynput 미설치" 경고
펫은 동작하지만 전역 키/마우스 감지가 꺼집니다. 수동 설치:
```bash
pip install pynput
```

### 회사 보안 EDR이 pynput을 차단
키후킹이 막힌 거예요. 펫 자체는 동작하고, 펫 직접 클릭 반응은 됩니다. 잠금/절전 감지(시간 점프 기반)도 영향 없음.

### 글자가 깨져 보임 (□ 박스 표시)
`tinypet/pet.py` 의 `font=("Malgun Gothic", 13, ...)` 를 다음 중 하나로 바꿔보세요:
- `"Segoe UI Emoji"`
- `"Segoe UI Symbol"`
- 시스템에 설치된 다른 한글+이모지 지원 글꼴

### 펫이 마젠타색 박스로 보임 (Windows)
글씨 색을 `#ff00ff` (마젠타) 와 비슷하게 설정하면 일부 글자도 같이 투명 처리됨. 우클릭 → "설정 초기화".

### 펫이 반투명 회색 박스로 보임 (Linux)
Linux는 per-color 투명을 지원하기 어려워서 `-alpha 0.9` 반투명 창으로 폴백합니다. 컴포지터(KWin/Mutter 등)가 켜져 있어야 알파가 적용돼요.

### macOS에서 펫이 흰 박스로 보임
`wm_attributes('-transparent', True)` 가 일부 Tk 빌드에서 무시될 수 있어요. Python 공식 빌드 권장:
```bash
brew install python-tk
```
또는 `python.org` 의 macOS installer 사용.

### macOS에서 외부 키/마우스 입력에 펫이 반응 안 함
접근성 권한 미설정. 시스템 설정 → 개인정보 보호 및 보안 → 접근성 → 사용 중인 앱(터미널 / TinyPet.app / Python) 체크.

### exe/.app 빌드 시 "_win32 / _darwin / _xorg 모듈을 못 찾음"
`pynput` 의 플랫폼별 모듈이 PyInstaller 자동 감지에 안 잡혀서 그래요. `build_exe.bat` / `build_app.sh` 에 이미 `--hidden-import` 옵션이 들어가 있습니다.
