[한국어](USAGE.md) · **English**

# Usage Guide

## Screen layout

```
┌─ user roam area (roam_box) ──┐
│                              │
│        ( ˙ㅅ˙ )             │  ← pet (text on transparent bg)
│                ( ˙ㅅ˙ )      │
│                              │
└──────────────────────────────┘
```

Default roam area is a 220×140 box in the top-right of your monitor. Changeable via the right-click menu.

---

## State machine

```
                    90s no input
   ┌──────────┐  ────────────────►  ┌──────────┐
   │  awake   │                      │  asleep  │
   │ peek /   │  ◄──────────────── │   zzZ    │
   │ jump /…  │   key/mouse input    └──────────┘
   └──────────┘                            │
        ▲                                  │ PC lock/sleep → wake
        │                                  │ (forced asleep + sleeping pose)
        └──────────────────────────────────┘
```

- **awake**: default. Looks around, plays random idle actions (jump/hearts/dance/etc.)
- **asleep**: sleepy. Only `( ˘ㅅ˘ )zzZ` looping.
- Transitions: any key/mouse → awake, 90s idle → asleep, PC unlocked → forced asleep.

---

## Right-click menu items

### Roam area
Define the rectangle where the pet wanders automatically.

- **↖ top-left**: drag pet to where you want, click → that point becomes the box's top-left
- **↘ bottom-right**: same for bottom-right
- **Reset**: back to default (top-right of screen)

### Text color
- 7 presets: Black / Dark gray (default) / White / Pastel pink / Mint / Sky blue / Mustard
- **Pick custom color...**: native Windows color picker
- ⚠️ Picking something close to `magenta(#ff00ff)` collides with the transparent color — letters may go invisible

### Speed
| Option | Multiplier |
|---|---|
| Very slow | ×2.0 |
| Slow | ×1.5 |
| **Normal (default)** | ×1.0 |
| Fast | ×0.65 |
| Very fast | ×0.4 |

Lower multiplier = faster. Applies to frame-display time and idle interval.

### Wake up / Sleep
- **Wake up now**: force awake (skip falling-asleep sequence)
- **Sleep now**: force asleep (plays falling-asleep sequence)

### Reset settings
Color / speed / roam-area all back to defaults. Settings file is rewritten.

### Quit
Closes pet. Current settings and position are saved one last time.

---

## Interactions

### Mouse
| Action | Effect |
|---|---|
| Left-click pet | Wave → smile → hearts → wink → both-hands wave → shy → music → clap → dance → phone (cycle) |
| Spam-click pet 6+ times in 5s | Angry → cools down |
| Spam-click pet 10+ times in 5s | Table-flip easter egg → resets table |
| Drag pet | Move position. Auto-saves on release. |
| Shake pet left-right while dragging (3+ direction changes) | Dizzy |
| Right-click pet | Menu |
| Click elsewhere (while asleep) | Pet startled |

Drag vs click distinction: any move > 4 pixels counts as drag.

### Keyboard
| Action | Effect |
|---|---|
| Any key (while asleep) | Wakes up |
| Any key (while awake) | Resets `last_input_time` (resets sleep countdown) |
| 90s no input | Dozes off |

---

## Animation list (39 total)

### Idle (randomly during awake)
- `looking_around`
- `head_tilt`
- `jump`, `bounce`
- `shrug`
- `wink`
- `thinking`
- `peek_a_boo`
- `shiver` (cold)
- `hot_pant` (hot)
- `look_back`
- `snack`
- `selfie`
- `run_right`, `run_left` (also used by wander for long moves)

### Joy / greeting (cycled on pet click)
- `wave`, `wave_both`
- `hearts`
- `smile_grow`
- `shy`
- `dance`
- `music`
- `clap`
- `phone`

### Emotion (rare idle / auto-chained)
- `crying` → `stop_crying`
- `fall_down` → `get_up`
- `run_and_hug` → `hug`

### Frustration (spam-click triggers)
- `angry` → `sulking_relief` (6+ rapid pet clicks)
- `table_flip` → `table_unflip` (10+ rapid pet clicks)

### Sleep
- `falling_asleep`
- `sleeping` (loops)
- `waking_up`

### Startled / dizzy
- `startled` (external click while asleep)
- `dizzy` (shake by dragging)

Each animation is a sequence of ~4 frames. During idle, animations are picked with weighted random — looking/head-tilt frequently, special actions rarely. Pairs marked with `→` auto-chain (the second plays after the first).

---

## Settings file

Location: `~/.tinypet.json`
Windows: `C:\Users\<username>\.tinypet.json`

### Format

```json
{
  "fg_color": "#222222",
  "speed": 1.0,
  "speed_key": "normal",
  "roam_box": [1680, 40, 1880, 180],
  "last_position": [1750, 100]
}
```

| Key | Meaning | Example |
|---|---|---|
| `fg_color` | Text color (hex) | `"#ff6f91"` |
| `speed` | Time multiplier (0.2–5.0) | `0.65` |
| `speed_key` | For radio button display | `"fast"` |
| `roam_box` | Roam area `[x1, y1, x2, y2]` | `[1680, 40, 1880, 180]` |
| `last_position` | Last position `[x, y]` | `[1750, 100]` |

### When it saves
- Color change (preset / picker)
- Speed change
- Roam area ↖/↘ / reset
- Pet drag to move (on release)
- Clean quit (right-click → Quit)

**Auto-moved positions are NOT saved** — only positions you set by drag are remembered.

### Manual edit
You can edit the JSON directly while the pet is closed. Invalid values are silently ignored (fallback to defaults).

### Reset
- Right-click → Reset settings
- Or delete the file: `del %USERPROFILE%\.tinypet.json` (Windows)

---

## Auto-start registration

### Windows — Startup folder (simple)
1. `Win+R` → `shell:startup` → Enter
2. Drop a **shortcut** of `TinyPet.exe` (or `run.bat`) into that folder

### Windows — Task Scheduler (more reliable)
1. Task Scheduler → "Create Basic Task"
2. Trigger: "When I log on"
3. Action: "Start a program" → path to `TinyPet.exe` (or `pythonw -m tinypet`)
4. "Run with highest privileges" usually unnecessary

### macOS
System Settings → General → Login Items → `+` → pick `TinyPet.app`.

### Linux
Add a `.desktop` file to `~/.config/autostart/`:
```ini
[Desktop Entry]
Type=Application
Name=TinyPet
Exec=python3 -m tinypet
Hidden=false
X-GNOME-Autostart-enabled=true
```
