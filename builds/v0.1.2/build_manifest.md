# Build Manifest - SnakeGradient v0.1.2 (Release)

## Build Metadata
- **Version**: 0.1.2
- **Build Date**: 2026-06-06
- **Platform**: Windows 11 (x64)
- **Build Tool**: PyInstaller 6.20.0
- **Python Version**: 3.11.9
- **Release Type**: Release Candidate 2 (Final)

## Package Contents
- **Executable**: `SnakeGradient_v0.1.2.exe` (One-File Bundle, 21.2MB)
- **Executable Path**: `builds/v0.1.2/executable/SnakeGradient_v0.1.2.exe`

## Bundled Artifacts
- **Assets**: `assets/` (BGM, SFX, Fonts, Images)
- **Localization**: `localization/en.json`
- **Configuration**: `src/systems/config.py` (Embedded)

## Release Artifacts
| Artifact | Path | Status |
|----------|------|--------|
| Executable | `builds/v0.1.2/executable/SnakeGradient_v0.1.2.exe` | ✅ |
| Changelog | `CHANGELOG.md` | ✅ |
| Release Notes | `RELEASE_NOTES_v0.1.2.md` | ✅ |
| Build Manifest | `builds/v0.1.2/build_manifest.md` | ✅ |
| QA Reports | `qa_reports/v0.1.2/` | ✅ |
| Screenshots | `screenshots/v0.1.2/` | ✅ |

## Validation Status
- **Playtest Bot**: PASS (All tests passed)
- **Stability Pass**: PASS (300s long-run: Avg FPS 10.01, Mem Growth 0.43MB)
- **Edge Case Spam**: PASS (500 iterations each)
- **Save/Load Stress**: PASS (1000 cycles)
- **State Cycle Stress**: PASS (200 cycles)
- **Behavioral Simulations**: PASS (All 9 profiles)
- **Accessibility Audit**: PASS (48 snapshots)
- **Visual Identity**: PASS (13 screens captured)

## RC2 Fixes Applied
1. **Void Theme Accessibility**: Added "void" to theme_keys in state_manager.py
2. **Boss Battle Pause**: Added ESC/P key handling to BOSS_BATTLE state
3. **Version Check**: Updated playtest bot version to 0.1.2

## Known Issues (Post-Release)
- Onboarding overlay timing needs investigation
- No per-mode leaderboard
- No achievement progress tracking
- Settings cycling UI (no sliders)
- No theme preview in shop

## Verdict
**RELEASE READY** ✅ - All critical issues resolved. Executable built, validated, and certified.