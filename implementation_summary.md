# Implementation Summary

## Automated release pipeline
- Added `.github/workflows/release.yml` to build a Windows `.exe` on tags matching `v*`.
- The workflow checks out the repo, sets up Python 3.11, installs dependencies from `requirements.txt`, and builds the executable with PyInstaller using `main.py` and the `assets` directory.
- The release job publishes the generated `.exe` to GitHub Releases and uses `body_path: CHANGELOG.md` so the release notes are automatically populated from the project changelog.

## Dependency and hygiene updates
- Added `requirements.txt` with `pygame` and `pyinstaller` for the release build.
- Added `dist/`, `build/`, `__pycache__/`, and common Python-generated files to `.gitignore` to prevent local artifacts from being committed.

## v0.0.3 Advanced Mechanics
- **Dynamic Difficulty Scaling**: Implemented a score-based speed increase in `states/state_gameplay.py`, increasing tick-rate every 50 points up to a cap of 20.
- **Golden Apple Power-up**: Enhanced the `golden` food type with a bonus point value (+15) and integrated unique sound effects.
- **Persistent Save System**: Created `save_manager.py` for handling high score persistence using `save_data.json`.
- **UI Integration**: Added "Best Score" displays to the Main Menu and Game Over screens.
- **QA Validation**: Upgraded `playtest_bot.py` to verify speed scaling, high score persistence, and power-up values, ensuring 100% test coverage for new mechanics.