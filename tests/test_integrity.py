# -*- coding: utf-8 -*-
"""TinyPet 정합성/로직 점검 (GUI 없이 실행)."""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tinypet.pet import (
    ANIMATIONS, IDLE_PICKS, CLICK_CYCLE, CHAIN_AFTER, TinyPet,
    FRAME_MS, IDLE_GAP_MS, IDLE_TO_SLEEP_SEC, LOCK_DETECT_SEC,
    PLATFORM, DEFAULT_FONT,
)

results = []

def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    results.append((status, name, detail))


# --- 1. ANIMATIONS 자체 구조 ---
for nm, frames in ANIMATIONS.items():
    check(f"ANIMATIONS[{nm}] is non-empty list",
          isinstance(frames, list) and len(frames) >= 1)
    check(f"ANIMATIONS[{nm}] all frames are str",
          all(isinstance(f, str) for f in frames))
check(f"animation count == 39", len(ANIMATIONS) == 39,
      f"actual: {len(ANIMATIONS)}")

# --- 2. 참조 정합성 ---
missing_idle = sorted(set(IDLE_PICKS) - set(ANIMATIONS))
check("all IDLE_PICKS in ANIMATIONS", not missing_idle,
      f"missing: {missing_idle}")

missing_click = [a for a in CLICK_CYCLE if a not in ANIMATIONS]
check("all CLICK_CYCLE in ANIMATIONS", not missing_click,
      f"missing: {missing_click}")

for k, v in CHAIN_AFTER.items():
    check(f"CHAIN_AFTER key '{k}' exists", k in ANIMATIONS)
    check(f"CHAIN_AFTER value '{v}' exists", v in ANIMATIONS)

# --- 3. 흔들기 감지 로직 ---
check("reversals: empty path = 0",
      TinyPet._count_reversals([]) == 0)
check("reversals: single direction = 0",
      TinyPet._count_reversals([100, 110, 120, 130, 140]) == 0)
check("reversals: 1 reversal (좌→우→좌)",
      TinyPet._count_reversals([100, 200, 100]) == 1,
      f"got {TinyPet._count_reversals([100, 200, 100])}")
check("reversals: tiny jitter ignored",
      TinyPet._count_reversals([100, 102, 101, 103, 102]) == 0)
check("reversals: shake detected (≥4)",
      TinyPet._count_reversals([100, 200, 100, 200, 100, 200]) >= 4)

# --- 4. 상수 sanity ---
check("FRAME_MS in reasonable range", 100 <= FRAME_MS <= 1000)
check("IDLE_GAP_MS in reasonable range", 500 <= IDLE_GAP_MS <= 3000)
check("IDLE_TO_SLEEP_SEC > LOCK_DETECT_SEC",
      IDLE_TO_SLEEP_SEC > LOCK_DETECT_SEC,
      f"idle_sleep={IDLE_TO_SLEEP_SEC}, lock_detect={LOCK_DETECT_SEC}")

# --- 5. 플랫폼 분기 ---
check(f"PLATFORM detected = {PLATFORM}",
      PLATFORM in ("win32", "darwin", "linux"))
check(f"DEFAULT_FONT set = {DEFAULT_FONT!r}", bool(DEFAULT_FONT))

# --- 출력 ---
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")
for status, name, detail in results:
    if status == "FAIL":
        print(f"  {status}  {name}   ({detail})")

print(f"\n{passed} passed, {failed} failed (of {len(results)})")
sys.exit(0 if failed == 0 else 1)
