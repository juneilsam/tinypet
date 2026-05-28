[한국어](INSTALL.md) · **English**

# Installation Guide

Three distribution forms. Pick the one that matches your environment.

| Form | Audience | Python required | Steps |
|---|---|---|---|
| **A. Click-to-Run** | End users | No | Download exe/app → double-click |
| **B. pip install** | Python users | 3.8+ | `pip install` then `tinypet` command |
| **C. Clone & Run** | Developers / local | 3.8+ | Clone, then `run.bat` / `./run.sh` |

---

## A. Click-to-Run

**Platforms**: Windows / macOS
**Python install**: not required

### Windows

1. Go to the [Releases page](https://github.com/juneilsam/tinypet/releases)
2. Download the latest `TinyPet.exe`
3. Save anywhere → double-click

You're good if the pet appears in the top-right of your screen sleeping as `( ˘ㅅ˘ )zzZ`.

**If Windows SmartScreen warns**: The exe isn't code-signed, so the first run shows "Windows protected your PC". Click "More info" → "Run anyway".

**Auto-start registration**:
1. `Win+R` → type `shell:startup` → Enter
2. Drop a **shortcut** to `TinyPet.exe` into the folder that opens (not the original file)

**Uninstall**: Delete the exe. To also clear settings:
```cmd
del %USERPROFILE%\.tinypet.json
```

### macOS

1. Download `TinyPet-macos.zip` from [Releases](https://github.com/juneilsam/tinypet/releases)
2. Unzip → double-click `TinyPet.app`

**If Gatekeeper blocks**: The app isn't signed/notarized, so it's blocked on first run.
- Right-click → **Open** → confirm **Open** in the dialog
- Or: System Settings → Privacy & Security → click **Open Anyway** next to the blocked-app notice

**Accessibility permission** (required for global key/mouse detection):
1. The system should pop up an access request on first run → allow it
2. If it doesn't: System Settings → Privacy & Security → Accessibility → toggle on `TinyPet`

Without this permission you'll only get: pet click reactions / lock-sleep detection / time-based dozing. (Waking via external key/click won't work.)

**Auto-start registration**: System Settings → General → Login Items → `+` → pick `TinyPet.app`.

**Uninstall**: Delete the app + settings file:
```bash
rm ~/.tinypet.json
```

### Linux

We don't ship prebuilt binaries (too many distros). Use **B** or **C** below.

---

## B. pip install

**Platforms**: Windows / macOS / Linux
**Required**: Python 3.8 or higher

On Linux you also need `python3-tk`:
- Debian / Ubuntu: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch: `sudo pacman -S tk`

### Check Python
```bash
python --version
```
Install Python 3.8+ from https://www.python.org/downloads/ if needed.

### Install

From GitHub:
```bash
pip install git+https://github.com/juneilsam/tinypet.git
```

### Run
```bash
tinypet
```
Or:
```bash
python -m tinypet
```

Background (no console window):
```bash
pythonw -m tinypet
```

### Update
```bash
pip install -U git+https://github.com/juneilsam/tinypet.git
```

### Uninstall
```bash
pip uninstall tinypet
```

---

## C. Clone & Run

**Platform**: Windows recommended
**Required**: Python 3.8+, git

### 1) Clone
```bash
git clone https://github.com/juneilsam/tinypet.git
cd tinypet
```

### 2-A) Helper script (recommended)

Windows:
```cmd
run.bat
```

macOS / Linux:
```bash
./run.sh
```

What it does (both):
- Checks for Python (+ tkinter on Linux)
- Auto-installs `pynput` if missing
- Runs in the background without a console (`pythonw -m tinypet` / `nohup ... &`)

### 2-B) Manual

```bash
pip install -r requirements.txt
python -m tinypet      # Windows
python3 -m tinypet     # macOS / Linux
```

Without console / terminal:
- Windows: `pythonw -m tinypet`
- macOS / Linux: `nohup python3 -m tinypet > /tmp/tinypet.log 2>&1 &`

Dev mode (instant reflection of code edits):
```bash
pip install -e .
tinypet
```

---

## Build your own binary (optional)

After cloning:

| Platform | Command | Output |
|---|---|---|
| Windows | `build_exe.bat` | `dist\TinyPet.exe` |
| macOS | `./build_app.sh` | `dist/TinyPet.app` |
| Linux | `./build_app.sh` | `dist/TinyPet` (single ELF binary) |

Roughly 30–40 MB single-file via PyInstaller `--onefile`.

---

## Troubleshooting

### "Python not found"
Python isn't installed or not on PATH. From https://www.python.org/downloads/, check "Add Python to PATH" during install.

### "pynput not installed" warning
The pet still works but global key/mouse detection is off. Install manually:
```bash
pip install pynput
```

### Corporate EDR blocks pynput
The keyhook is blocked. The pet itself still runs, and direct pet-click responses work. Lock/sleep detection (time-jump based) is also unaffected.

### Characters appear broken (□ boxes)
Edit `tinypet/pet.py` and change `DEFAULT_FONT` for your platform:
- Try `"Segoe UI Emoji"` / `"Segoe UI Symbol"` on Windows
- Make sure the chosen font supports Korean + math symbols + emoji

### Pet shows as a magenta block (Windows)
You probably set the text color close to `#ff00ff` (magenta), which gets treated as transparent. Right-click → "Reset settings".

### Pet shows as a translucent gray block (Linux)
Linux can't easily do per-color transparency, so we fall back to an `-alpha 0.9` translucent window. Your compositor (KWin / Mutter / etc.) must be enabled for alpha to apply.

### Pet shows as a white block on macOS
`wm_attributes('-transparent', True)` may be ignored by some Tk builds. Use the official Python build:
```bash
brew install python-tk
```
or grab the macOS installer from python.org.

### Pet doesn't react to external keys/mouse on macOS
Accessibility permission not granted. System Settings → Privacy & Security → Accessibility → tick your active app (Terminal / TinyPet.app / Python).

### Build error: "module _win32 / _darwin / _xorg not found"
PyInstaller's auto-detection misses pynput's platform module. `build_exe.bat` / `build_app.sh` already include the right `--hidden-import` flags.
