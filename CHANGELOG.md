# Changelog

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