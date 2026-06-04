# Changelog

## [0.0.2] - 2026-06-04
### Changed
- Refactored asset pipeline: reorganized assets into assets/images, assets/sfx, assets/bgm, assets/fonts, and assets/screenshots; added idempotent migration logic to move legacy files.
- Implemented AssetManager singleton with caching for images, sounds and fonts; added robust path fallbacks and generated placeholder surfaces for missing images.
- Reskinned UI with a dark premium theme: rounded corners, hover/press glow, improved typography and subtle animated markers.
- Updated the automated playtest bot to use cached AssetManager names, capture runtime screenshots to assets/screenshots/, and validate UI bounding boxes.
- Added snapshot automation and an expanded diagnostic matrix for end-to-end QA; fixed ShopUI grid selection bug.

### Fixed
- Improved sound/image path fallback to avoid run-time asset failures (missing apple.png now handled).
- Minor dead-code/log cleanup and safer mixer/font fallbacks for headless/CI environments.

## [0.0.1] - 2026-06-04
### Added
- Initial Modular Architecture.
- Menu Overhaul (Concept 1 layout).
- Audio Integration.
- Premium Skin Shop.
- Vision-Based Automated QA Testing Bot (Dev-Only).