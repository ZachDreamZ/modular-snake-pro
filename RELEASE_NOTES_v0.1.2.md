# Release Notes - SnakeGradient v0.1.2

## Overview
Version 0.1.2 (Release Candidate 2) focuses on real player simulation, feedback integration, and critical bug fixes identified during RC1 testing. This release addresses all critical issues found during extensive player persona testing and edge case validation.

## New Features
- **Player Persona Testing**: 5 distinct personas simulated (First-Time Player, Casual, Competitive High-Score, Achievement Hunter, Long-Session Player)
- **Real Player Behavior Simulation**: Button spamming, rapid menu switching, settings abuse, rapid restart, save/load abuse, pause/unpause abuse
- **Edge Case Validation**: Minimum/maximum progression states, unusual settings combinations, boundary values, input sequence edge cases
- **Boss Battle Pause**: Players can now pause during boss fights using ESC or P keys
- **Void Theme Accessibility**: The Void theme is now properly available in the shop

## UI Improvements
- Enhanced onboarding flow for first-time players
- Improved pause menu accessibility during boss encounters
- Consistent visual identity across all 13 key screens

## Gameplay Improvements
- Boss battles now support pause/resume functionality
- All 6 themes properly accessible through the shop system
- Enhanced stability with 300s long-run validation

## Bug Fixes
- **Void Theme Unobtainable (FIXED)**: Added "void" to theme_keys in state_manager.py - previously unobtainable theme now available in shop
- **Boss Battle Pause (FIXED)**: Added ESC/P key handling to BOSS_BATTLE state - players can now pause during boss fights
- **Version Check (FIXED)**: Playtest bot version check updated from 0.1.1 to 0.1.2

## Performance Improvements
- Long-run stability: Avg FPS 10.01, Memory growth 0.43MB over 300s
- Edge case spam: 500 iterations each (menu, pause, settings, restart) - all PASS
- State cycle stress: 200 cycles without crash
- Save/load stress: 1000 cycles without corruption

## Technical Changes
- 10 new playtest bot tests for RC2 validation
- Test matrix expanded with boss pause handling, void theme accessibility, onboarding reliability
- All 9 behavioral player profiles simulated with extended 1000-frame sessions
- Accessibility audit: 48 snapshots captured across all font scale and colorblind mode combinations

## Known Issues
- Onboarding overlay timing needs investigation for first-launch reliability
- No per-mode leaderboard (planned for post-RC2)
- No achievement progress tracking (planned for post-RC2)
- Settings cycling UI (no sliders) - minor UX friction
- No theme preview in shop (planned for post-RC2)
- No session timer display
- Game speed caps early with no further scaling