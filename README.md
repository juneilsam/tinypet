<div align="right">

**한국어** · [English](README.en.md)

</div>

<div align="center">

# TinyPet

### 화면 한 켠에서 두리번거리는, 작고 귀여운 텍스트 데스크탑 펫

지루한 회사의 업무, 삭막한 사무실, 고통스러운 내 자리.

스트레스와 화를 억누르며 탈출만 갈망하고 계신 건 아닌가요?

아무도 모르게 화면 안에서 두리번거리고, 졸기도 하고, 가끔 책상도 뒤집으며 — 나만의 작은 위안이 되어 줄

**✨ 작고 귀여운 텍스트 펫을 키워 보세요 ✨**

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#설치-방법)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter%20(stdlib)-success.svg)](https://docs.python.org/3/library/tkinter.html)

<img src="assets/demo.gif" alt="TinyPet 데모" width="600">

```
   ( ˙ㅅ˙ )            ( ˙ㅅ˙ )ノ            ( ˘ㅅ˘ )zzZ
   두리번거리다가       클릭하면 인사하고       90초 두면 새근새근
```

```
   (♡ㅅ♡ )            (╯｀ㅅ´)╯︵┻━┻          ( @ㅅ@ )～
   예뻐하면 하트뿅       마구 누르면 책상 뒤집기     흔들면 어지러워해요
```

</div>

- 다른 창 위에 떠 있는 **투명 오버레이** (Windows: 진짜 투명 / macOS: 시스템 투명 / Linux: 반투명)
- **39가지 텍스트 애니메이션** — 두리번/점프/하트/춤/까꿍/셀카/달리기 등
- **반응형 상호작용** — 클릭 / 빠른 연타(화남·테이블뒤집기) / 흔들기(어지러움) / 드래그
- **PC 잠금/절전에서 깨면** 자고 있는 모습으로 맞이
- **사용자 지정 산책 영역** — 우클릭으로 영역 지정
- **글씨 색·속도 커스터마이즈** + 설정 자동 저장 (`~/.tinypet.json`)
- **크로스플랫폼**: Windows / macOS / Linux

---

## 설치 방법

자기에게 맞는 한 가지를 고르세요. 자세한 가이드: [docs/INSTALL.md](docs/INSTALL.md)

### A. 단순 실행형 (가장 쉬움)

Python 설치 필요 없음. [Releases](https://github.com/juneilsam/tinypet/releases) 에서:

| 플랫폼 | 파일 | 실행 |
|---|---|---|
| Windows | `TinyPet.exe` | 더블클릭 |
| macOS | `TinyPet-macos.zip` | 압축 풀고 `TinyPet.app` 더블클릭 |
| Linux | (pip 또는 빌드) | 아래 B/C |

### B. 터미널 설치형 — Python 사용자

```bash
pip install git+https://github.com/juneilsam/tinypet.git
tinypet
```

### C. 터미널 실행형 — 개발자 / 로컬 실행

```bash
git clone https://github.com/juneilsam/tinypet.git
cd tinypet

run.bat           # Windows
./run.sh          # macOS / Linux
```

수동:
```bash
pip install -r requirements.txt
python -m tinypet     # Windows
python3 -m tinypet    # macOS / Linux
```

**macOS 추가 권한**: 전역 키/마우스 감지(`pynput`)는 *시스템 설정 → 개인정보 보호 및 보안 → 접근성* 에서 터미널(또는 TinyPet.app) 허용 필요.

---

## 사용법

마우스 하나면 충분해요 — 클릭하면 인사하고, 흔들면 어지러워하고, 너무 괴롭히면 책상을 뒤집어요. 자세히: [docs/USAGE.md](docs/USAGE.md)

### 상호작용

| 동작 | 결과 |
|---|---|
| 펫 좌클릭 | 인사/하트/스마일 등 (사이클로 변함) |
| 펫 빠르게 6번+ 연타 | 화남 → 풀림 |
| 펫 빠르게 10번+ 연타 | 테이블 뒤집기 이스터에그 |
| 펫 좌우로 흔들기 | 어지러움 |
| 펫 드래그 | 위치 이동 (자동 저장) |
| 펫 우클릭 | 메뉴 |
| 키 입력 (잠든 중) | 일어나기 |
| 화면 다른 곳 클릭 (잠든 중) | 깜짝 |
| 90초간 입력 없음 | 졸다가 잠 |
| PC 잠금/절전 → 깸 | 자고 있는 모습으로 시작 |

### 우클릭 메뉴

- **산책영역 ↖/↘** — 펫을 원하는 위치로 드래그 → 우클릭으로 박스의 두 모서리 지정
- **글씨 색깔** — 프리셋 7색 + 직접 고르기 (컬러피커)
- **움직임 속도** — 아주 느림 ~ 아주 빠름 (5단계)
- **지금 깨우기 / 재우기** — 강제 상태 전환
- **설정 초기화** — 기본값으로
- **종료**

---

## 설정 파일

위치: `~/.tinypet.json` (Windows: `C:\Users\<user>\.tinypet.json`)

```json
{
  "fg_color": "#222222",
  "speed": 1.0,
  "speed_key": "normal",
  "roam_box": [1680, 40, 1880, 180],
  "last_position": [1750, 100]
}
```

저장 시점: 색·속도·산책영역 변경 / 드래그로 이동 / 정상 종료. 펫이 자동으로 움직인 위치는 저장 안 함.

---

## 자동 시작 등록

한 번 등록해두면 부팅할 때마다 조용히 함께 출근해요.

- **Windows**: `Win+R` → `shell:startup` → 열린 폴더에 `TinyPet.exe` (또는 `run.bat`) **바로가기** 복사
- **macOS**: 시스템 설정 → 일반 → 로그인 항목 → `+` → `TinyPet.app`
- **Linux**: 데스크톱 환경의 자동 시작 폴더에 `.desktop` 파일 추가 (보통 `~/.config/autostart/`)

---

## FAQ

**Q. 회사 PC에 깔아도 되나요?**
무해한 오버레이 창이지만, 전역 키후킹(`pynput`)이 보안 EDR에 차단될 수 있어요. 차단돼도 펫 자체는 동작합니다 (펫 직접 클릭 반응만).

**Q. 화면 공유할 때 안 보이게?**
우클릭 → 종료. 항상 위(topmost) 옵션이라 회의 전엔 끄세요.

**Q. macOS / Linux 도 되나요?**
네. 플랫폼별로 투명 처리 방식이 다릅니다:
- **Windows**: 마젠타 픽셀을 진짜 투명 처리 (글자만 보임)
- **macOS**: `wm_attributes('-transparent')` + `bg='systemTransparent'` (진짜 투명)
- **Linux**: per-color 투명 어려움 → 반투명 창(`-alpha 0.9`)으로 폴백
macOS는 pynput 사용 시 *접근성* 권한 필요. Linux는 컴포지터(KWin/Mutter 등)가 켜져 있어야 알파가 적용됩니다.

**Q. 글자가 깨져요.**
기본 글꼴은 플랫폼별로 다릅니다 (Win: Malgun Gothic / macOS: Apple SD Gothic Neo / Linux: Noto Sans CJK KR). `tinypet/pet.py` 의 `DEFAULT_FONT` 를 시스템에 설치된 다른 글꼴로 바꿔보세요.

---

## 개발

[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) 참고. 빌드, 새 애니메이션 추가, 릴리스 절차 등.

```bash
git clone https://github.com/juneilsam/tinypet.git
cd tinypet
pip install -e ".[build]"
python -m tinypet
```

---

## 변경 이력

[CHANGELOG.md](CHANGELOG.md)

## 라이선스

[MIT](LICENSE)
