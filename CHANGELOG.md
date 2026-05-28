# Changelog

All notable changes to TinyPet are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-05-28

### Added
- 39 text-based animations (looking around, sleeping, dancing, hearts, peek-a-boo,
  selfie, running, crying/recovery, falling/getting up, table flip easter egg, etc.)
- Transparent overlay window
  - Windows: true per-color transparency via `-transparentcolor`
  - macOS: `wm_attributes('-transparent')` with `systemTransparent` bg
  - Linux: fallback to translucent window (`-alpha 0.9`)
- State machine: awake / asleep with auto-dozing after 90s of no input
- PC lock/sleep detection via wall-clock jump (no pywin32 dependency)
- User-defined roam area via right-click menu
- Customization
  - Text color: 7 presets + native color picker
  - Speed: 5 presets (×0.4 to ×2.0)
- Reactive interactions
  - Pet left-click: cycles through wave/hearts/smile/wink/etc.
  - Rapid 6+ clicks in 5s: angry → relief
  - Rapid 10+ clicks in 5s: table flip easter egg
  - Drag shake (4+ direction reversals): dizzy
- Settings persistence at `~/.tinypet.json`
- Distribution
  - Single-file Windows `.exe` and macOS `.app` via PyInstaller
  - pip installable (`pip install git+https://github.com/...`)
  - `run.bat` / `run.sh` helper scripts with auto dep install
- GitHub Actions: automatic builds + releases on tag push
- Cross-platform: Windows / macOS / Linux
- Documentation: README, INSTALL, USAGE, DEVELOPMENT (Korean + English)
