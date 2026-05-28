[한국어](DEVELOPMENT.md) · **English**

# Developer Guide

## Environment setup

```bash
git clone https://github.com/juneilsam/tinypet.git
cd tinypet

# Virtualenv (optional but recommended)
python -m venv .venv
.venv\Scripts\activate         # Windows
# source .venv/bin/activate    # macOS / Linux

# Editable install + build tools
pip install -e ".[build]"
```

Run:
```bash
python -m tinypet
```

Edit code → restart pet to see changes.

---

## File structure

```
tinypet/
├── tinypet/                      # Python package
│   ├── __init__.py               # version, public API
│   ├── __main__.py               # python -m tinypet entry point
│   └── pet.py                    # main code (TinyPet class, main function)
├── docs/
│   ├── INSTALL.md / .en.md       # install details
│   ├── USAGE.md / .en.md         # usage details
│   └── DEVELOPMENT.md / .en.md   # this doc
├── .github/workflows/
│   └── release.yml               # builds Win exe + macOS .app on tag push
├── pyproject.toml                # package metadata + dependencies
├── requirements.txt              # runtime dependency list
├── run.bat / run.sh              # auto-install deps + background run
├── build_exe.bat / build_app.sh  # PyInstaller build
├── README.md / README.en.md
├── LICENSE                       # MIT
└── .gitignore
```

---

## Code structure (`tinypet/pet.py`)

| Section | Role |
|---|---|
| `PLATFORM`, `DEFAULT_FONT` | Platform detection (sys.platform), default font per OS |
| `ANIMATIONS` | Action name → list of frames (text). All expressions/motions defined here |
| `IDLE_PICKS`, `CLICK_CYCLE` | Random pool for idle, cycle for clicks |
| Timing constants (`FRAME_MS`, `IDLE_TO_SLEEP_SEC`, etc.) | Timing parameters |
| `TinyPet.__init__` | Tk window, widgets, state variables, menu, key/mouse listeners |
| `TinyPet._setup_transparency()` | Platform-specific transparent background setup |
| `TinyPet.tick()` | Main loop — detects wall-clock jumps, plays frames, decides next action |
| `wake_up()`, `force_sleep()` | Force mode changes |
| `on_press/drag/release` | Mouse on pet (drag vs click) |
| `_kb_cb`, `_mouse_cb` | pynput callbacks (background thread → `root.after(0, ...)` to main thread) |
| `wander()` | Move to random position within roam area |
| `set_color()`, `set_speed()`, `pick_color()` | Customization |
| `_load/save/apply_config()` | `~/.tinypet.json` persistence |

### Key design points
- **Single-thread GUI**: pynput callbacks run on a background thread → marshaled to the main thread via `root.after(0, ...)`
- **PC lock/sleep detection**: detected via wall-clock jump (`time.time()` difference) instead of OS APIs → no pywin32 dependency
- **Cross-platform transparency**:
  - Windows: `tk.attributes("-transparentcolor", "magenta")` for per-pixel
  - macOS: `wm_attributes("-transparent", True)` + `bg='systemTransparent'`
  - Linux: fallback to `-alpha 0.9` translucent window

---

## Adding a new animation

1. Add an entry to the `ANIMATIONS` dict:
   ```python
   "new_action": ["( ˙ㅅ˙ )", "( ⊙ㅅ⊙ )", "( ˙ㅅ˙ )"],
   ```
2. Pick where to trigger it:
   - **Randomly during idle**: add the action name to `IDLE_PICKS` (weight = number of occurrences)
   - **On pet click cycle**: add to `CLICK_CYCLE`
   - **On a specific event**: call `self.enqueue("new_action")` in the relevant handler

Each frame displays for `FRAME_MS` (350ms, scaled by speed multiplier).

---

## Building

### Local binaries

| Platform | Command | Output |
|---|---|---|
| Windows | `build_exe.bat` | `dist\TinyPet.exe` |
| macOS | `./build_app.sh` | `dist/TinyPet.app` |
| Linux | `./build_app.sh` | `dist/TinyPet` |

About 30–40 MB.

### GitHub Actions auto-build
Pushing a tag starting with `v` triggers `.github/workflows/release.yml`:
1. Builds on Windows runner → `TinyPet.exe`
2. Builds on macOS runner → `TinyPet-macos.zip`
3. Both attached to a GitHub Release

```bash
git tag v0.1.0
git push origin v0.1.0
```

---

## Testing

GUI app → automated tests are limited. Manual checklist:

- [ ] Pet appears in sleeping state on startup
- [ ] Pet wakes and starts cycle animation on left-click
- [ ] External key input wakes pet (sleeping → waking_up)
- [ ] External click startles pet (sleeping → startled)
- [ ] 90s no input transitions to falling_asleep → sleeping
- [ ] PC sleep/lock → wake forces sleeping state
- [ ] Drag and click are distinguished (4-pixel threshold)
- [ ] All right-click menu items work
- [ ] Color/speed/roam-area persist across restart
- [ ] Corrupted settings file falls back to defaults

### Cross-platform checks
- [ ] Windows: magenta background goes transparent (only text visible)
- [ ] macOS: pet shows on transparent system background
- [ ] macOS: Accessibility permission flow works
- [ ] Linux: translucent window appears (compositor enabled)

---

## Release process

1. **Bump version**
   - `tinypet/__init__.py` → `__version__`
   - `pyproject.toml` → `version`
2. **Update changelog / README** as needed
3. **Commit & tag**
   ```bash
   git commit -am "release: v0.x.y"
   git tag v0.x.y
   git push && git push origin v0.x.y
   ```
4. **Verify auto-build**
   - Check the build job passes in GitHub Actions
   - Confirm exe / .app.zip appear on the Release page

---

## Contributing

Issues and Pull Requests welcome. For larger changes, please open an issue to discuss first.

### Good PR ideas
- New animations
- Better Linux transparency (per-pixel via compositor hints)
- Time-based modes (snacks at lunchtime, dance at quitting time, etc.)
- Keyboard shortcut to toggle pet visibility
- System tray icon (right-click menu access when window isn't visible)
- More languages (i18n)
