# -*- coding: utf-8 -*-
"""TinyPet - 화면 한 켠에서 두리번거리는 텍스트 펫.

실행:
    python -m tinypet
    또는
    tinypet            (pip 설치 후)
종료:
    펫 우클릭 -> 종료
선택 의존성:
    pip install pynput   (없어도 동작은 하지만 전역 키/마우스 감지가 꺼짐)

플랫폼 메모:
    Windows: -transparentcolor 로 마젠타 픽셀이 진짜 투명
    macOS:   wm_attributes('-transparent') + bg='systemTransparent'
    Linux:   진짜 투명 어려움 → -alpha 0.9 (반투명 창) 로 폴백
"""
import json
import os
import random
import sys
import time
import tkinter as tk
from tkinter import colorchooser

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".tinypet.json")
PLATFORM = sys.platform  # 'win32', 'darwin', 'linux'

# 플랫폼별 기본 글꼴 (Tk 글꼴 폴백이 부족할 때를 대비)
if PLATFORM == "win32":
    DEFAULT_FONT = "Malgun Gothic"
elif PLATFORM == "darwin":
    DEFAULT_FONT = "Apple SD Gothic Neo"
else:
    DEFAULT_FONT = "Noto Sans CJK KR"

try:
    from pynput import keyboard, mouse
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False


ANIMATIONS = {
    # 평상시
    "looking_around": ["( ˙ㅅ˙ )", "(  ˙ㅅ˙)", "(˙ㅅ˙  )", "( ˙ㅅ˙ )"],
    "head_tilt":      ["( ˙ㅅ˙ )", "( ˙ㅅ˙　)", "(　˙ㅅ˙ )", "( ˙ㅅ˙ )"],
    "jump":           ["( ˙ㅅ˙ )", "⸜( ˙ㅅ˙ )⸝", "( ˙ㅅ˙ )", "⸜( ˙ㅅ˙ )⸝"],
    "bounce":         ["( ˙ㅅ˙ )", "( ˙ㅅ˙ )ノ", "⸜(˙ㅅ˙ )⸝", "( ˙ㅅ˙ )"],
    "shrug":          ["( ˙ㅅ˙ )", "¯\\( ˙ㅅ˙ )/¯", "( ˙ㅅ˙ )", "¯\\( ˙ㅅ˙ )/¯"],
    "wink":           ["( ˙ㅅ˙ )", "( ˙ㅅ< )", "( -ㅅ< )", "( ˙ㅅ˙ )"],
    "thinking":       ["( ˙ㅅ˙ )", "( ˙ㅅ˙ )｡oO", "( ’ㅅ’ )｡oO", "( ˙ㅅ˙ )!💡"],
    "peek_a_boo":     ["|˙ㅅ˙ )", "|　˙ㅅ˙ )", "|　　　 ", "( ˙ㅅ˙ )!"],
    "shiver":         ["( ˙ㅅ˙ )", "( ˙ㅅ˙;)", "((( ˙ㅅ˙ )))", "((( >ㅅ< )))"],
    "snack":          ["( ˙ㅅ˙ )🍙", "( ˙ڡ˙ )🍙", "( ˙ㅅ˙ )", "( ˘ㅅ˘ )♡"],
    "selfie":         ["( ˙ㅅ˙ )📷", "( ˙ㅅ< )📷", "( ˙▿˙ )✧📷", "( ◕▿◕ )📸"],

    # 인사/기쁨 (펫 클릭 시 사이클)
    "wave":           ["( ˙ㅅ˙ )ノ", "( ˙ㅅ˙ )ﾉ", "( ˙ㅅ˙ )/", "( ˙ㅅ˙ )ヽ"],
    "wave_both":      ["ヽ( ˙ㅅ˙ )ノ", "＼( ˙ㅅ˙ )／", "ヽ( ˙ㅅ˙ )ノ", "＼( ˙ㅅ˙ )／"],
    "hearts":         ["( ˙ㅅ˙ )", "( ˙ㅅ˙ )♡", "( ˙ㅅ˙ )♡♡", "(♡ㅅ♡ )"],
    "smile_grow":     ["( ˙ㅅ˙ )", "( ˙▿˙ )", "( ◕▿◕ )", "(≧▽≦)"],
    "shy":            ["( ˙ㅅ˙ )", "( //ㅅ// )", "(/ㅅ＼)", "(*ﾉㅅﾉ)"],
    "dance":          ["⸜( ˙ㅅ˙ )⸝", "⸝( ˙ㅅ˙ )⸜", "⸜( ˙ㅅ˙ )⸝", "⸝( ˙ㅅ˙ )⸜"],
    "music":          ["( ˙ㅅ˙ )", "♪( ˙ㅅ˙ )", "♪( ˙▿˙ )♪", "♬⸜(˙▿˙ )⸝♬"],
    "clap":           ["( ˙ㅅ˙ )", "( ˙ㅅ˙ )👏", "👏( ˙ㅅ˙ )👏", "( ˙▿˙ )👏"],

    # 잠
    "falling_asleep": ["( ˙ㅅ˙ )", "( -ㅅ˙ )", "( -ㅅ- )", "( ˘ㅅ˘ )zzZ"],
    "sleeping":       ["( ˘ㅅ˘ )zzZ", "( ˘ㅅ˘ )zZ ", "( ˘ㅅ˘ )z  ", "( ˘ㅅ˘ )zZ "],
    "waking_up":      ["( ˘ㅅ˘ )zzZ", "( -ㅅ- )", "( ˙ㅅ- )", "( ˙ㅅ˙ )!"],

    # 깜짝 / 어지러움
    "startled":       ["( ˙ㅅ˙ )", "( °ㅅ° )!!", "( ˙ㅅ˙;)", "( ˙ㅅ˙ )～"],
    "dizzy":          ["( @ㅅ@ )", "( ×ㅅ× )～", "( @ㅅ@ )～～", "( ˙ㅅ˙;)"],

    # 감정 (확장)
    "crying":         ["( ˙ㅅ˙ )", "( ˙ㅅ˙; )", "( ;ㅅ; )", "( ╥ㅅ╥ )"],
    "stop_crying":    ["( ╥ㅅ╥ )", "( ;ㅅ; )", "( ’ㅅ’ )", "( ˙ㅅ˙ )✧"],
    "angry":          ["( ˙ㅅ˙ )", "( ˙ㅅ˙# )", "( ｀ㅅ´ )", "( ╬｀ㅅ´)"],
    "sulking_relief": ["( ¬ㅅ¬ )", "( ｀ㅅ´ )", "( ˙ㅅ˙ )", "( ˙▿˙ )"],
    "hot_pant":       ["( ˙ㅅ˙ )", "( ˙ㅅ˙;)", "( ˙ㅂ˙;)", "( ˙ﻝ˙;)💦"],

    # 동작 (확장)
    "run_right":      ["( ˙ㅅ˙ )=3", "　ε=( ˙ㅅ˙ )", "　　ε=( ˙ㅅ˙ )", "　　　ε=( ˙ㅅ˙ )"],
    "run_left":       ["　　　( ˙ㅅ˙ )=ɜ", "　　( ˙ㅅ˙ )=ɜ", "　( ˙ㅅ˙ )=ɜ", "( ˙ㅅ˙ )"],
    "run_and_hug":    ["ε=( ˙ㅅ˙ )", "　ε=( ˙ㅅ˙ )", "　　(っ˙ㅅ˙)っ", "　　(っ˙ㅅ˙)っ♡"],
    "hug":            ["( ˙ㅅ˙ )　( ˙ㅅ˙ )", "( ˙ㅅ˙)( ˙ㅅ˙ )", "(っ˙ㅅ˙)づ˙ㅅ˙ )", "(づ˙ㅅ˙)づ♡"],
    "look_back":      ["( ˙ㅅ˙ )", "( ˙ㅅ )", "( ˙ )", "( ㅅ˙ )"],

    # 이벤트 / 이스터에그
    "phone":          ["( ˙ㅅ˙ )📱", "( ˙ㅅ˙)📱", "( ˙ㅅ˙☎)", "( ˙▿˙☎)"],
    "table_flip":     ["( ˙ㅅ˙ )", "( ｀ㅅ´ )", "(╯｀ㅅ´)╯︵┻━┻", "( ˙ㅅ˙ )…"],
    "table_unflip":   ["︵┻━┻", "┬─┬ ノ( ˙ㅅ˙ノ)", "┬─┬", "( ˙ㅅ˙ )✧"],
    "fall_down":      ["( ˙ㅅ˙ )", "( ˙ㅅ˙)?", "( ˙ㅅ˙ )〴", "＿(˙ㅅ˙」∠)＿"],
    "get_up":         ["＿(˙ㅅ˙」∠)＿", "( ˙ㅅ˙〴 )", "( ˙ㅅ˙;)", "( ˙ㅅ˙ )"],
}

# idle 시 무작위로 뽑는 풀 (가중치는 중복으로 표현)
IDLE_PICKS = (
    ["looking_around"] * 5
    + ["head_tilt"] * 3
    + ["jump", "bounce", "shrug", "wink"]
    + ["thinking", "peek_a_boo", "music", "dance", "hearts", "snack", "selfie", "shiver"]
    # 확장
    + ["hot_pant", "look_back", "run_right", "run_left"]
    # 희귀 (체인되는 감정/동작)
    + ["crying", "fall_down", "hug", "run_and_hug"]
)

# 펫을 클릭할 때마다 돌아가는 사이클
CLICK_CYCLE = [
    "wave", "smile_grow", "hearts", "wink",
    "wave_both", "shy", "music", "clap", "dance", "phone",
]

# 어떤 액션 다음에 자동으로 뒤따라 재생할지 (예: 울었으면 그치기까지 같이 보여줌)
CHAIN_AFTER = {
    "fall_down":   "get_up",
    "crying":      "stop_crying",
    "table_flip":  "table_unflip",
    "angry":       "sulking_relief",
    "run_and_hug": "hug",
}

FRAME_MS = 350           # 한 프레임 표시 시간
IDLE_GAP_MS = 1200       # 액션 사이 쉬는 시간
WANDER_EVERY = 5         # 평균 idle N회마다 자리 이동
IDLE_TO_SLEEP_SEC = 90   # 입력 없이 N초 -> 졸다가 잠
LOCK_DETECT_SEC = 60     # tick 간격이 이만큼 벌어지면 PC가 잠들어있었다고 판단
TRANS_COLOR = "magenta"  # 이 색이 투명 처리됨 (Windows 전용)
DEFAULT_ROAM_W = 220     # 기본 산책 영역 가로
DEFAULT_ROAM_H = 140


class TinyPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("tinypet")
        self.root.overrideredirect(True)
        try:
            self.root.attributes("-topmost", True)
        except tk.TclError:
            pass

        # 플랫폼별 투명 배경 설정 (배경색 문자열을 반환)
        self._bg = self._setup_transparency()

        self.fg_color = "#222222"   # 글씨 색 (기본 = 매우 짙은 회색)
        self.label = tk.Label(
            self.root,
            text=ANIMATIONS["sleeping"][0],
            font=(DEFAULT_FONT, 13, "bold"),
            fg=self.fg_color,
            bg=self._bg,
            cursor="hand2",
            padx=4, pady=2,
        )
        self.label.pack()

        # 상태
        self.mode = "asleep"        # asleep | awake
        self.queue = []             # 재생 대기 프레임 [(face, hold_ms), ...]
        self.last_input_time = 0.0  # 0 = 한참 전 -> 시작 시 sleep 유지
        self.last_tick_wall = time.time()
        self.idle_loops = 0
        self.click_idx = 0
        self.click_times = []       # 최근 클릭 시각 (연타 감지용)
        self.speed = 1.0            # 시간 배수: 1.0=보통, 낮을수록 빠름

        # 산책 영역 기본 = 화면 우상단
        sw = self.root.winfo_screenwidth()
        self.roam_box = (sw - DEFAULT_ROAM_W - 40, 40,
                         sw - 40, 40 + DEFAULT_ROAM_H)
        cx = (self.roam_box[0] + self.roam_box[2]) // 2
        cy = (self.roam_box[1] + self.roam_box[3]) // 2
        self.root.geometry(f"+{cx}+{cy}")

        # 마우스 바인딩 (드래그 vs 클릭 구분)
        self._drag_origin = None
        self._dragged = False
        self._drag_path = []        # 드래그 중 x좌표 샘플 (흔들기 감지용)
        # 흔드는 "도중" 실시간 어지러움 표현
        self._live_dizzy_until = 0.0   # 이 시각까지 어지러운 표정 유지
        self._live_dizzy_idx = 0       # 어지러움 프레임 순환 인덱스
        self._reversal_times = []      # 최근 방향전환 시각 (1초 윈도우)
        self._live_dir = 0             # 실시간 현재 진행 방향
        self._live_last_x = None       # 마지막으로 데드존 넘은 x
        self.label.bind("<Button-1>", self.on_press)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.on_release)
        self.label.bind("<Button-3>", self.on_right_click)

        # 우클릭 메뉴
        m = tk.Menu(self.root, tearoff=0)
        m.add_command(label="현재 위치를 산책영역 ↖ 좌상단으로", command=self.set_roam_topleft)
        m.add_command(label="현재 위치를 산책영역 ↘ 우하단으로", command=self.set_roam_bottomright)
        m.add_command(label="산책영역 화면 우상단으로 리셋", command=self.reset_roam)
        m.add_separator()

        # 글씨 색
        color_menu = tk.Menu(m, tearoff=0)
        for label, hex_ in [
            ("검정",                "#000000"),
            ("짙은 회색 (기본)",    "#222222"),
            ("흰색 (어두운 배경)",  "#ffffff"),
            ("파스텔 핑크",          "#ff6f91"),
            ("민트",                "#3ec1a7"),
            ("하늘색",               "#4a90e2"),
            ("머스타드",             "#d4a72c"),
        ]:
            color_menu.add_command(label=label, command=lambda c=hex_: self.set_color(c))
        color_menu.add_separator()
        color_menu.add_command(label="색깔 직접 고르기...", command=self.pick_color)
        m.add_cascade(label="글씨 색깔", menu=color_menu)

        # 움직임 속도
        self.speed_var = tk.StringVar(value="normal")
        speed_menu = tk.Menu(m, tearoff=0)
        for label, key, mult in [
            ("아주 느림", "very_slow", 2.0),
            ("느림",      "slow",      1.5),
            ("보통",      "normal",    1.0),
            ("빠름",      "fast",      0.65),
            ("아주 빠름", "very_fast", 0.4),
        ]:
            speed_menu.add_radiobutton(
                label=label, variable=self.speed_var, value=key,
                command=lambda v=mult: self.set_speed(v),
            )
        m.add_cascade(label="움직임 속도", menu=speed_menu)

        m.add_separator()
        m.add_command(label="지금 깨우기", command=lambda: self.wake_up(force=True))
        m.add_command(label="지금 재우기", command=self.force_sleep)
        m.add_separator()
        m.add_command(label="설정 초기화", command=self.reset_settings)
        m.add_command(label="종료", command=self.quit)
        self.menu = m

        # 저장된 설정 불러오기 (메뉴/변수 다 만들어진 뒤에)
        self._apply_config(self._load_config())

        # 전역 입력 (백그라운드 스레드 -> root.after 로 마샬링)
        self.kb_listener = None
        self.mouse_listener = None
        if HAS_PYNPUT:
            self.kb_listener = keyboard.Listener(on_press=self._kb_cb, daemon=True)
            self.mouse_listener = mouse.Listener(on_click=self._mouse_cb, daemon=True)
            self.kb_listener.start()
            self.mouse_listener.start()

        # 시작: 자고 있는 모습으로
        self.enqueue("sleeping")
        self.root.after(int(FRAME_MS * self.speed), self.tick)

    # ---------- 플랫폼별 투명 처리 ----------
    def _setup_transparency(self):
        """플랫폼별 투명 배경을 시도하고 사용할 bg 문자열을 반환."""
        if PLATFORM == "win32":
            try:
                self.root.attributes("-transparentcolor", TRANS_COLOR)
                self.root.configure(bg=TRANS_COLOR)
                return TRANS_COLOR
            except tk.TclError:
                pass
        elif PLATFORM == "darwin":
            try:
                self.root.wm_attributes("-transparent", True)
                self.root.configure(bg="systemTransparent")
                return "systemTransparent"
            except tk.TclError:
                pass
        else:
            # Linux 등: per-color 투명은 어려우니 반투명 창으로 폴백
            try:
                self.root.attributes("-alpha", 0.9)
            except tk.TclError:
                pass
        # 폴백 / Linux 기본 배경
        bg = "#f5f5f5"
        try:
            self.root.configure(bg=bg)
            return bg
        except tk.TclError:
            return self.root.cget("bg")

    # ---------- 큐 / 렌더 ----------
    def enqueue(self, action, frame_ms=None):
        if frame_ms is None:
            frame_ms = int(FRAME_MS * self.speed)
        for face in ANIMATIONS[action]:
            self.queue.append((face, frame_ms))

    def render(self, face):
        self.label.config(text=face)

    # ---------- 메인 틱 ----------
    def tick(self):
        # 1. PC가 잠들었다 깬 경우 감지 (after 타이머가 그동안 멈춰 있었음)
        now = time.time()
        gap = now - self.last_tick_wall
        self.last_tick_wall = now
        if gap > LOCK_DETECT_SEC:
            self.queue.clear()
            self.mode = "asleep"
            self.last_input_time = 0.0
            self.render(ANIMATIONS["sleeping"][0])
            self.root.after(int(FRAME_MS * self.speed * 3), self.tick)
            return

        # 1.5 흔드는 도중이면 실시간으로 어지러운 표정 (큐보다 우선)
        if now < self._live_dizzy_until:
            faces = ANIMATIONS["dizzy"][:3]
            self.render(faces[self._live_dizzy_idx % len(faces)])
            self._live_dizzy_idx += 1
            self.root.after(int(FRAME_MS * self.speed * 0.5), self.tick)
            return

        # 2. 재생할 프레임이 있으면 그것부터
        if self.queue:
            face, hold = self.queue.pop(0)
            self.render(face)
            self.root.after(hold, self.tick)
            return

        # 3. 큐 비었음 -> 다음 행동 결정
        if self.mode == "asleep":
            self.enqueue("sleeping")
            self.root.after(int(IDLE_GAP_MS * self.speed), self.tick)
            return

        # awake
        idle_since = now - self.last_input_time
        if idle_since > IDLE_TO_SLEEP_SEC:
            self.mode = "asleep"
            self.enqueue("falling_asleep")
            self.root.after(int(FRAME_MS * self.speed), self.tick)
            return

        self.idle_loops += 1
        ran_far = False
        if self.idle_loops % WANDER_EVERY == 0:
            ran_far = self.wander()
        if not ran_far:
            action = random.choice(IDLE_PICKS)
            self.enqueue(action)
            if action in CHAIN_AFTER:
                self.enqueue(CHAIN_AFTER[action])
        self.root.after(int(IDLE_GAP_MS * self.speed), self.tick)

    # ---------- 깨우기 / 재우기 ----------
    def wake_up(self, force=False, startled=False):
        if self.mode == "awake" and not force:
            return
        self.mode = "awake"
        self.last_input_time = time.time()
        self.queue.clear()
        self.enqueue("startled" if startled else "waking_up")

    def force_sleep(self):
        self.mode = "asleep"
        self.last_input_time = 0.0
        self.queue.clear()
        self.enqueue("falling_asleep")

    # ---------- 펫 직접 상호작용 ----------
    def on_press(self, event):
        self._drag_origin = (event.x_root, event.y_root,
                             self.root.winfo_x(), self.root.winfo_y())
        self._dragged = False
        self._drag_path = [event.x_root]
        self._reversal_times = []
        self._live_dir = 0
        self._live_last_x = event.x_root

    def on_drag(self, event):
        if not self._drag_origin:
            return
        ox, oy, wx, wy = self._drag_origin
        dx, dy = event.x_root - ox, event.y_root - oy
        if abs(dx) > 4 or abs(dy) > 4:
            self._dragged = True
        self.root.geometry(f"+{wx + dx}+{wy + dy}")
        self._drag_path.append(event.x_root)
        if len(self._drag_path) > 40:
            self._drag_path.pop(0)
        # 흔드는 도중 실시간 어지러움: 1초 안에 방향전환 2회+ 면 표정 갱신
        if self._live_last_x is not None:
            sd = event.x_root - self._live_last_x
            if sd > 3 or sd < -3:
                cur = 1 if sd > 0 else -1
                if self._live_dir and cur != self._live_dir:
                    now = time.time()
                    self._reversal_times.append(now)
                    self._reversal_times = [t for t in self._reversal_times if now - t <= 1.0]
                    if len(self._reversal_times) >= 2:
                        self._live_dizzy_until = now + 0.5
                self._live_dir = cur
                self._live_last_x = event.x_root

    def on_release(self, event):
        was_dragged = self._dragged
        path = self._drag_path
        self._drag_origin = None
        self._dragged = False
        self._drag_path = []
        if was_dragged:
            # 흔들기 감지: x축 방향 전환 3회 이상이면 어지러움
            if self._count_reversals(path) >= 3:
                self.queue.clear()
                self.enqueue("dizzy")
            self._save_config()  # 드래그로 옮긴 위치 저장
            return
        # 진짜 클릭
        self.last_input_time = time.time()
        self.queue.clear()
        if self.mode == "asleep":
            self.mode = "awake"
            self.enqueue("waking_up")
            return
        # 빠른 연타 감지
        now = time.time()
        self.click_times = [t for t in self.click_times if now - t < 5.0]
        self.click_times.append(now)
        if len(self.click_times) >= 10:
            # 극한 연타 → 테이블 뒤집기 이스터에그
            self.click_times.clear()
            self.enqueue("table_flip")
            self.enqueue("table_unflip")
        elif len(self.click_times) >= 6:
            # 짜증 → 화났다가 풀림
            self.click_times.clear()
            self.enqueue("angry")
            self.enqueue("sulking_relief")
        else:
            action = CLICK_CYCLE[self.click_idx % len(CLICK_CYCLE)]
            self.click_idx += 1
            self.enqueue(action)

    def on_right_click(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    @staticmethod
    def _count_reversals(path):
        """드래그 경로의 좌우 방향 전환 횟수 (작은 흔들림은 무시)."""
        if len(path) < 3:
            return 0
        count = 0
        prev_dir = 0
        for i in range(1, len(path)):
            d = path[i] - path[i - 1]
            if d > 3:
                cur = 1
            elif d < -3:
                cur = -1
            else:
                continue
            if prev_dir != 0 and cur != prev_dir:
                count += 1
            prev_dir = cur
        return count

    # ---------- 전역 입력 콜백 (pynput 스레드) ----------
    def _kb_cb(self, key):
        self.root.after(0, self._handle_global, False)

    def _mouse_cb(self, x, y, button, pressed):
        if not pressed:
            return
        # 펫 창 위 클릭은 자체 핸들러가 처리하므로 무시
        try:
            wx, wy = self.root.winfo_x(), self.root.winfo_y()
            ww, wh = self.root.winfo_width(), self.root.winfo_height()
            if wx <= x <= wx + ww and wy <= y <= wy + wh:
                return
        except Exception:
            pass
        self.root.after(0, self._handle_global, True)

    def _handle_global(self, is_click):
        was_asleep = self.mode == "asleep"
        self.last_input_time = time.time()
        if was_asleep:
            self.queue.clear()
            self.mode = "awake"
            self.enqueue("startled" if is_click else "waking_up")

    # ---------- 산책 ----------
    def wander(self):
        """랜덤 위치로 이동. 큰 가로 이동이면 달리기 모션 재생 후 텔레포트.

        반환값:
            True  - 달리기 모션이 큐에 들어갔으니 이번 tick은 추가 idle 액션 생략
            False - 즉시 텔레포트만 했으니 idle 액션 추가 진행
        """
        x1, y1, x2, y2 = self.roam_box
        ww = max(self.root.winfo_width(), 80)
        wh = max(self.root.winfo_height(), 30)
        max_x = max(x1 + 1, x2 - ww)
        max_y = max(y1 + 1, y2 - wh)
        nx = random.randint(min(x1, max_x), max_x)
        ny = random.randint(min(y1, max_y), max_y)

        cur_x = self.root.winfo_x()
        if abs(nx - cur_x) > 80:
            anim = "run_right" if nx > cur_x else "run_left"
            self.enqueue(anim)
            delay = (int(IDLE_GAP_MS * self.speed)
                     + len(ANIMATIONS[anim]) * int(FRAME_MS * self.speed))
            self.root.after(delay, lambda x=nx, y=ny: self.root.geometry(f"+{x}+{y}"))
            return True
        self.root.geometry(f"+{nx}+{ny}")
        return False

    def set_roam_topleft(self):
        x, y = self.root.winfo_x(), self.root.winfo_y()
        _, _, x2, y2 = self.roam_box
        self.roam_box = (min(x, x2 - 60), min(y, y2 - 40),
                         max(x + 60, x2), max(y + 40, y2))
        self._save_config()

    def set_roam_bottomright(self):
        x, y = self.root.winfo_x(), self.root.winfo_y()
        x1, y1, _, _ = self.roam_box
        self.roam_box = (min(x1, x - 60), min(y1, y - 40),
                         max(x1 + 60, x), max(y1 + 40, y))
        self._save_config()

    def reset_roam(self):
        sw = self.root.winfo_screenwidth()
        self.roam_box = (sw - DEFAULT_ROAM_W - 40, 40,
                         sw - 40, 40 + DEFAULT_ROAM_H)
        self._save_config()

    # ---------- 모양 / 속도 ----------
    def set_color(self, hex_color):
        self.fg_color = hex_color
        self.label.config(fg=hex_color)
        self._save_config()

    def pick_color(self):
        # askcolor 는 ((r,g,b), '#rrggbb') 또는 (None, None) 반환
        result = colorchooser.askcolor(
            initialcolor=self.fg_color,
            title="펫 글씨 색 고르기",
            parent=self.root,
        )
        if result and result[1]:
            self.set_color(result[1])

    def set_speed(self, multiplier):
        self.speed = max(0.2, min(5.0, float(multiplier)))
        self._save_config()

    def reset_settings(self):
        try:
            os.remove(CONFIG_PATH)
        except OSError:
            pass
        self.set_color("#222222")
        self.speed_var.set("normal")
        self.set_speed(1.0)
        self.reset_roam()

    # ---------- 설정 저장/로드 ----------
    def _load_config(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}

    def _save_config(self):
        data = {
            "fg_color": self.fg_color,
            "speed": self.speed,
            "speed_key": self.speed_var.get(),
            "roam_box": list(self.roam_box),
            "last_position": [self.root.winfo_x(), self.root.winfo_y()],
        }
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"[tinypet] 설정 저장 실패: {e}")

    def _apply_config(self, cfg):
        if not isinstance(cfg, dict):
            return
        if isinstance(cfg.get("fg_color"), str):
            self.fg_color = cfg["fg_color"]
            self.label.config(fg=self.fg_color)
        if "speed" in cfg:
            try:
                self.speed = max(0.2, min(5.0, float(cfg["speed"])))
            except (TypeError, ValueError):
                pass
        if isinstance(cfg.get("speed_key"), str):
            try:
                self.speed_var.set(cfg["speed_key"])
            except Exception:
                pass
        rb = cfg.get("roam_box")
        if isinstance(rb, (list, tuple)) and len(rb) == 4:
            try:
                self.roam_box = tuple(int(v) for v in rb)
            except (TypeError, ValueError):
                pass
        pos = cfg.get("last_position")
        if isinstance(pos, (list, tuple)) and len(pos) == 2:
            try:
                self.root.geometry(f"+{int(pos[0])}+{int(pos[1])}")
            except (TypeError, ValueError):
                pass

    def quit(self):
        try:
            self._save_config()
        except Exception:
            pass
        try:
            if self.kb_listener:
                self.kb_listener.stop()
            if self.mouse_listener:
                self.mouse_listener.stop()
        except Exception:
            pass
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    """콘솔 스크립트 / `python -m tinypet` / 직접 실행 공통 진입점."""
    if not HAS_PYNPUT:
        print("Warning: pynput 미설치 -> 전역 키/마우스 감지가 꺼집니다.")
        print("  설치: pip install --user pynput")
    TinyPet().run()


if __name__ == "__main__":
    main()
