# 🐍 SnakeGradient - Modular Snake Pro

[![Release](https://img.shields.io/badge/release-v0.1.2-blue)](https://github.com/ZachDreamZ/modular-snake-pro/releases/tag/v0.1.2)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-green)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/pygame-2.6.1-orange)](https://www.pygame.org/)

A premium, modular evolution of the classic Snake game, featuring a robust state-driven architecture, a diverse theme shop, advanced AI-driven boss battles, and professional UI/UX design.

## 🎮 Game Modes

| Mode | Description |
|------|-------------|
| **Classic** | The timeless experience with escalating speed and boss encounters |
| **Time Rush** | Race against the clock - eat food to extend your timer |
| **Maze Hell** | Start deep in the challenge with advanced stage constraints |
| **Endless** | Infinite gameplay with no boss battles - how long can you survive? |
| **Hardcore** | High-speed mode with boss battles at maximum intensity |
| **Survival** | Test your endurance in a pure survival challenge |

## ✨ Features

### Gameplay
- **6 Game Modes** - Classic, Time Rush, Maze Hell, Endless, Hardcore, Survival
- **Boss Battles** - Face off against an AI-driven Mecha-Snake Boss with unique attack patterns
- **Combo System** - Chain food eats for multiplier bonuses up to 3.0x
- **Frenzy Mode** - Triggered at 10+ combo for enhanced gameplay
- **Ghost Mode** - Temporary body collision immunity
- **6 Food Types** - Normal, Golden, Poison, Shield, Missile, Ghost
- **Stage Progression** - Dynamic difficulty scaling with obstacle generation
- **AI Opponent** - Advanced pathfinding AI snake

### Visual & UI
- **Professional UI Framework** - PressStart2P typography, beveled borders, dynamic glow effects
- **6 Visual Themes** - Classic Arcade, Cyberpunk Neon, Retro GameBoy, Golden Mecha, Ghost, The Void
- **Theme Shop** - Collect points to unlock high-rarity skins (Common, Epic, Legendary)
- **Colorblind Support** - Protanopia, Deuteranopia, Tritanopia palettes
- **Font Scaling** - 1.0x to 1.5x for accessibility
- **Screen Shake** - Impact feedback for food, power-ups, and death
- **Particle Effects** - Visual feedback for all game events

### Progression
- **Achievement System** - 11 achievements including First Blood, Dragon Slayer, Void Walker
- **Objectives System** - 8 objectives with reward points and persistence
- **Leaderboard** - High score tracking with stage information
- **Persistent Stats** - Games played, boss wins, food eaten, max combo
- **Save/Load** - Full game state persistence

### Accessibility
- **Colorblind Modes** - 3 colorblind palettes
- **Font Scaling** - Adjustable text size
- **Localization** - JSON-based language system
- **Mod Support** - Custom theme loading system

## 🖼️ Visual Previews

| Main Menu | Theme Shop |
| :---: | :---: |
| ![Main Menu Screen](assets/screenshots/main_menu.png) | ![Theme Shop Screen](assets/screenshots/skin_shop.png) |

| Gameplay | Boss Battle |
| :---: | :---: |
| ![Gameplay Preview](assets/screenshots/gameplay.png) | ![Boss Battle](assets/screenshots/boss_battle.png) |

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Pygame 2.6.1+

### Installation
```bash
pip install -r requirements.txt
```

### Execution
```bash
python main.py
```

### Controls
| Key | Action |
|-----|--------|
| WASD / Arrow Keys | Move snake |
| ESC / P | Pause |
| Space | Confirm / Select |
| Enter | High score entry confirm |

## 🛠️ Development & Testing

### Automated QA Bot
The project includes a comprehensive `playtest_bot.py` that performs:
- Audio pipeline and asset loading verification
- State machine transition validation
- Snake movement, growth, and collision testing
- UI hover/press/shop purchase logic testing
- Boss system spawn and state transition testing
- Combo, ghost, frenzy, and achievement mechanics testing
- 9 behavioral player profiles (Aggressive, Passive, Completionist, etc.)
- Edge case spam testing (menu, pause, settings, restart)
- Long-run stability testing (300s+)
- Save/load stress testing (1000+ cycles)
- Accessibility audit (48 snapshot combinations)
- Visual identity verification (13 screens)

```bash
python -m src.tools.playtest_bot
```

### Production Build
```bash
pyinstaller --onefile --add-data "assets;assets" --add-data "localization;localization" src/main.py --name SnakeGradient_v0.1.2
```

## 📦 Release Artifacts

```
builds/v0.1.2/
├── executable/
│   └── SnakeGradient_v0.1.2.exe
├── assets/
├── logs/
├── build_manifest.md
└── SnakeGradient_v0.1.2.spec
```

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for full version history.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of contributors.

## 🏗️ Project Structure

```
src/
├── main.py                    # Entry point
├── gameplay/
│   ├── entities.py            # Snake, Food, Boss entities
│   └── states/
│       ├── state_manager.py   # State machine
│       ├── state_menu.py      # Menu state
│       ├── state_gameplay.py  # Gameplay state
│       └── state_shop.py      # Shop state
├── systems/
│   ├── config.py              # Game configuration
│   ├── game_assets.py         # Asset management
│   ├── save_manager.py        # Save/load system
│   ├── progression_manager.py # Progression system
│   ├── localization_manager.py# Localization
│   └── analytics_manager.py   # Analytics
├── tools/
│   └── playtest_bot.py        # QA testing bot
└── ui/
    ├── __init__.py
    └── ui.py                  # UI components
```

## 🔗 Links

- **GitHub**: https://github.com/ZachDreamZ/modular-snake-pro
- **Releases**: https://github.com/ZachDreamZ/modular-snake-pro/releases
- **Issues**: https://github.com/ZachDreamZ/modular-snake-pro/issues