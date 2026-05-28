**한국어** · [English](DEVELOPMENT.en.md)

# 개발자 가이드

## 환경 셋업

```bash
git clone https://github.com/juneilsam/tinypet.git
cd tinypet

# 가상환경 (선택, 권장)
python -m venv .venv
.venv\Scripts\activate         # Windows
# source .venv/bin/activate    # macOS/Linux

# 개발 모드 설치 + 빌드 도구
pip install -e ".[build]"
```

실행:
```bash
python -m tinypet
```

코드 수정 후 펫만 재시작하면 즉시 반영.

---

## 파일 구조

```
tinypet/
├── tinypet/                      # 파이썬 패키지
│   ├── __init__.py               # 버전, 공개 API
│   ├── __main__.py               # python -m tinypet 진입점
│   └── pet.py                    # 본체 (TinyPet 클래스, main 함수)
├── docs/
│   ├── INSTALL.md                # 설치 상세
│   ├── USAGE.md                  # 사용 상세
│   └── DEVELOPMENT.md            # 이 문서
├── .github/workflows/
│   └── release.yml               # 태그 푸시 시 exe 빌드 + 릴리스
├── pyproject.toml                # 패키지 메타데이터 + 의존성
├── requirements.txt              # 단순 실행 의존성 목록
├── run.bat                       # 의존성 자동 설치 + 백그라운드 실행
├── build_exe.bat                 # PyInstaller 빌드 스크립트
├── README.md
├── LICENSE                       # MIT
└── .gitignore
```

---

## 코드 구조 (`tinypet/pet.py`)

| 섹션 | 역할 |
|---|---|
| `ANIMATIONS` | 액션 이름 → 프레임(텍스트) 리스트. 모든 표정/모션이 여기 정의 |
| `IDLE_PICKS`, `CLICK_CYCLE` | idle 무작위 풀, 클릭 사이클 |
| 상수 (`FRAME_MS`, `IDLE_TO_SLEEP_SEC` 등) | 타이밍 관련 |
| `TinyPet.__init__` | Tk 창, 위젯, 상태 변수, 메뉴, 키보드/마우스 리스너 |
| `TinyPet.tick()` | 메인 루프. wall-clock 점프 감지 → 프레임 재생 → 다음 행동 결정 |
| `wake_up()`, `force_sleep()` | 모드 강제 전환 |
| `on_press/drag/release` | 펫 위 마우스 (드래그/클릭 구분) |
| `_kb_cb`, `_mouse_cb` | pynput 콜백 (백그라운드 스레드 → `root.after(0, ...)` 로 메인 스레드 위임) |
| `wander()` | 산책 영역 안에서 무작위 위치로 이동 |
| `set_color()`, `set_speed()`, `pick_color()` | 커스터마이즈 |
| `_load/save/apply_config()` | `~/.tinypet.json` 영속화 |

### 핵심 설계 포인트
- **단일 스레드 GUI**: pynput은 별도 스레드에서 콜백을 호출하므로 `root.after(0, ...)` 로 메인 스레드에 위임
- **PC 잠금/절전 감지**: 별도 OS API 안 쓰고 wall-clock 점프 (`time.time()` 차이) 로 감지 → pywin32 의존성 없음
- **투명 배경**: Windows 전용 `tk.attributes("-transparentcolor", "magenta")` 사용

---

## 새 애니메이션 추가

1. `ANIMATIONS` dict에 항목 추가:
   ```python
   "new_action": ["( ˙ㅅ˙ )", "( ⊙ㅅ⊙ )", "( ˙ㅅ˙ )"],
   ```
2. 트리거 위치 정하기:
   - **idle 중 무작위로**: `IDLE_PICKS` 리스트에 액션 이름 추가 (가중치 = 등장 횟수)
   - **펫 클릭 시 사이클에**: `CLICK_CYCLE` 리스트에 추가
   - **특정 이벤트에서**: 해당 핸들러 안에서 `self.enqueue("new_action")`

각 프레임은 `FRAME_MS` (350ms, 속도 배수 적용) 동안 표시.

---

## 빌드

### 로컬 exe 빌드
```cmd
build_exe.bat
```
결과: `dist\TinyPet.exe` (대략 30~40MB)

### GitHub Actions 자동 빌드
`v` 로 시작하는 태그를 푸시하면 `.github/workflows/release.yml` 가 자동으로:
1. Windows runner에서 PyInstaller 빌드
2. `dist\TinyPet.exe` 를 GitHub Releases에 첨부

```bash
git tag v0.1.0
git push origin v0.1.0
```

---

## 테스트

GUI 앱이라 자동화는 제한적. 수동 체크리스트:

- [ ] 시작 시 sleeping 상태로 뜨는지
- [ ] 펫 좌클릭 시 awake로 전환되고 사이클 액션이 재생되는지
- [ ] 외부 키 입력 시 (잠든 상태 → waking_up) 동작
- [ ] 외부 클릭 시 (잠든 상태 → startled) 동작
- [ ] 90초간 입력 없을 때 falling_asleep → sleeping 으로 가는지
- [ ] PC 절전/잠금 → 깸 시 강제로 sleeping 으로 가는지
- [ ] 드래그와 클릭이 구분되는지 (4픽셀 임계값)
- [ ] 우클릭 메뉴 모든 항목이 동작하는지
- [ ] 색/속도/산책영역 변경 후 재시작 시 유지되는지
- [ ] 설정 파일 손상 시 기본값으로 fallback 되는지

---

## 릴리스 절차

1. **버전 업데이트**
   - `tinypet/__init__.py` 의 `__version__`
   - `pyproject.toml` 의 `version`
2. **변경 사항 정리**
   - README / CHANGELOG (있다면)
3. **커밋 & 태그**
   ```bash
   git commit -am "release: v0.x.y"
   git tag v0.x.y
   git push && git push origin v0.x.y
   ```
4. **자동 빌드 확인**
   - GitHub Actions의 build job 통과 확인
   - Releases 페이지에 `TinyPet.exe` 첨부됐는지 확인

---

## 기여

이슈 / Pull Request 환영. 큰 변경은 이슈로 먼저 논의 부탁드립니다.

자주 받기 좋은 PR:
- 새 애니메이션 추가
- macOS / Linux 투명 배경 대안
- 시간대별 모드 (점심엔 간식 자주, 등)
- 단축키 토글 (펫 숨기기/보이기)
- 트레이 아이콘 (창 안 보일 때 우클릭 메뉴 진입)
