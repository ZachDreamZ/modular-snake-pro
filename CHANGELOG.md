# Changelog

## [0.1.3] - 2026-06-06
### Added
- Release notes for v0.1.2
- MIT License and CONTRIBUTORS.md
- .gitignore
### Changed
- Professional README.md and LICENSE formatting
- Implementation summary and build manifest updates for v0.1.2 release

## [0.1.2] - 2026-06-06
### Added
- Player persona testing with 5 distinct personas (First-Time, Casual, Competitive, Achievement Hunter, Long-Session)
- Real player behavior simulation (button spamming, rapid menu switching, settings abuse)
- Edge case validation for minimum/maximum progression states
- Boss battle pause support (ESC/P key handling)
- Void theme accessibility in shop (added to theme_keys)
- 10 new playtest bot tests for RC2 validation

### Changed
- Version bumped from 0.1.1 to 0.1.2
- Playtest bot version check updated to 0.1.2
- Enhanced stability testing: 300s long-run, 500 edge case iterations, 200 state cycles, 1000 save/load cycles

### Fixed
- Void theme now accessible in shop (was missing from theme_keys)
- Boss battle now supports pause (ESC/P key handling added)
- Onboarding overlay timing investigation documented

## [0.1.1] - 2026-06-05
### Added
- Unified visual identity system with UITheme class (Primary, Secondary, Accent, Success, Warning, Danger roles)
- Enhanced UI components: role-based button coloring, professional beveled borders, multi-layered outer glow
- Standardized UIPanel and UIProgressBar with role-based coloring
- Professional typography hierarchy (Huge, Medium, Small, Tiny)
- Visual identity test suite in playtest bot with comprehensive screenshot capture
- Balance refinement pass for difficulty curves and reward economy

### Changed
- All UI components migrated to UITheme system for consistent styling
- Gameplay HUD refined with new color palette and layout
- Shop, Game Over, Victory screens standardized to new visual language
- Navigation back buttons unified with DANGER role

### Fixed
- Visual consistency across all 13 key screens verified
- Layout inconsistencies in menu navigation resolved

## [0.1.0] - 2026-06-05
### Added
- Professional UI framework with PressStart2P-Regular.ttf typography
- Enhanced Button class with beveled borders, dynamic glow, hover/press scaling
- New UI components: UIPanel, UIProgressBar
- Shop UI overhaul with card layouts and spacing
- Relative layout system for menus (centered positioning)
- Grouped settings (Audio, Visual, General) in UIPanels
- Cinematic title presentation and visual hierarchy
- Integrated gameplay HUD with dispersed layout (score, stage, timer, combo)
- High-impact end screens (Game Over, Victory, High Score Entry)
- Dynamic difficulty scaling with non-linear speed growth
- Score balancing with 3.0x max combo multiplier
- Screen shake system for food, power-ups, and death
- 9 behavioral playtest profiles (Aggressive, Passive, Completionist, etc.)

### Changed
- Version bumped from 0.0.9 to 0.1.0
- Menu navigation expanded with Stats -> Achievements/Objectives flow
- All hardcoded strings replaced with localization keys

### Fixed
- Mode select back button stability
- Attribute errors on rapid state transitions

## [0.0.9] - 2026-06-04
### Added
- Stage announcement overlay system
- Enhanced toast notifications with points display
- Ding sound for notifications
- Input buffering for smoother controls
- Snake bounce effect on food eat
- Death flash effect on collision
- Cleanup pass for code quality

### Changed
- Version bumped from 0.0.8 to 0.0.9

### Fixed
- Various UI/UX polish items

## [0.0.8] - 2026-06-04
### Added
- Mandatory executable certification pipeline with PyInstaller
- Automated executable validation (startup, runtime, shutdown, save integrity)
- Build certification report generation (build_certification_report_v0.0.8.md)
- 3 new playtest bot tests: analytics logging, settings persistence, shutdown cleanup (28 total)
- Release gate enforcement with certification requirements
- Executable validation script (validate_executable.py)

### Changed
- Version bumped from 0.0.7 to 0.0.8
- Playtest bot test matrices updated to V008 prefix
- All version references updated across test infrastructure

### Fixed
- Version check test updated to validate 0.0.8

## [0.0.7] - 2026-04-06
### Added
- Weighted food spawning system (6 food types with configurable probabilities)
- 3 new achievements: Combo Master, Point Collector, Unstoppable (8 total)
- Objectives system: 5 objectives with reward points and persistence
- Contextual hints for first-time players and mode introductions
- Persistent stats tracking (games played, boss wins, food eaten, max combo)
- Stats, Achievements, and Objectives screens in the menu
- Time Rush HUD timer display with low-time warning
- Config-based balancing parameters (FOOD_SCORES, spawn weights, combo thresholds)
- 10 new playtest bot tests for v0.0.7 features (25 tests total)

### Changed
- Menu navigation expanded with Stats -> Achievements/Objectives flow
- Food spawning uses weighted random selection instead of hardcoded ratios
- Leaderboard now shows stage information
- Localization expanded with 15 new keys

### Fixed
- Mode select back button stability
- Shield collision handling in boss battles
- Attribute errors on rapid state transitions

## [0.0.6] - 2026-03-30
### Added
- Settings system with Music, SFX, Font Scale, Colorblind Mode, Language
- Font scaling (1.0x to 1.5x) for accessibility
- Colorblind support (Protanopia, Deuteranopia, Tritanopia palettes)
- Localization framework with JSON-based system
- Mod loading system for custom themes
- Advanced analytics (session tracking, death analysis, theme usage)

### Changed
- All hardcoded strings replaced with localization keys
- Theme application integrated with mod system
- Settings persist to settings.json

## [0.0.5] - 2026-03-20
### Added
- Boss battle system with Mecha-Snake Boss
- Combo system with multiplier and frenzy mode
- Ghost mode for body collision immunity
- Void Walker achievement for Maze Hell mode
- Stage progression with obstacle generation
- Dynamic difficulty scaling
- Particle effects for food collection

### Changed
- Enhanced AI snake pathfinding
- Improved visual effects and animations

## [0.0.4] - 2026-03-10
### Added
- Maze Hell game mode
- Shop system with theme purchases
- Leaderboard functionality
- Time Rush game mode
- AI Snake opponent

## [0.0.3] - 2026-03-01
### Added
- Multiple food types (golden, poison, shield, missile, ghost)
- Stage system with obstacle generation
- Basic achievement system (First Blood, Marathon, Dragon Slayer, Speed Demon)

## [0.0.2] - 2026-02-20
### Added
- Basic gameplay loop
- Snake movement and collision
- Food collection
- Score tracking
- High score persistence

## [0.0.1] - 2026-02-15
### Added
- Initial project setup
- Pygame initialization
- Basic window rendering