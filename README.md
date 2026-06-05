<div align="center">

# 🐍 SnakeGradient

### *A Premium Modular Snake Game with Professional UI/UX*

[![Release](https://img.shields.io/github/v/release/ZachDreamZ/modular-snake-pro?color=blue&label=Release&style=for-the-badge)](https://github.com/ZachDreamZ/modular-snake-pro/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1%2B-green?style=for-the-badge&logo=pygame&logoColor=white)](https://www.pygame.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011-0078D4?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Maintenance](https://img.shields.io/badge/Maintained-Yes-brightgreen?style=for-the-badge)](https://github.com/ZachDreamZ/modular-snake-pro/commits/main)

*A modern evolution of the classic Snake game, featuring 6 game modes, AI-driven boss battles, a complete progression system, and a polished arcade aesthetic.*

[**🚀 Download Latest Release**](https://github.com/ZachDreamZ/modular-snake-pro/releases/latest) · [**📖 Documentation**](#-table-of-contents) · [**🐛 Report Bug**](https://github.com/ZachDreamZ/modular-snake-pro/issues) · [**💡 Request Feature**](https://github.com/ZachDreamZ/modular-snake-pro/issues)

---

</div>

## 📑 Table of Contents

- [🎯 About The Project](#-about-the-project)
- [✨ Features](#-features)
- [🎮 Game Modes](#-game-modes)
- [🖼️ Screenshots](#-screenshots)
- [🛠️ Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [🎮 Controls](#-controls)
- [🏗️ Architecture](#-architecture)
- [🧪 Testing](#-testing)
- [📦 Building](#-building)
- [📋 Changelog](#-changelog)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👥 Authors](#-authors)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🎯 About The Project

**SnakeGradient** is a premium, modular evolution of the classic Snake game that goes far beyond simple grid-based gameplay. Built with a robust state-driven architecture, it offers a complete arcade experience with multiple game modes, AI-driven boss battles, a fully-featured theme shop, and a comprehensive progression system.

### Why SnakeGradient?

- 🎮 **6 Distinct Game Modes** - From classic to hardcore survival
- 🤖 **AI-Driven Boss Battles** - Intelligent enemies with unique attack patterns
- 🎨 **6 Visual Themes** - Including legendary rarity skins
- 🏆 **Achievement System** - 11 achievements to unlock
- 📊 **Persistent Statistics** - Track your progress across sessions
- ♿ **Accessibility First** - Colorblind support, font scaling, localization

---

## ✨ Features

<div align="center">

| Category | Features |
|----------|----------|
| 🎮 **Gameplay** | 6 game modes, AI boss battles, combo system, frenzy mode, ghost mode, 6 food types, stage progression, AI opponent |
| 🎨 **Visual & UI** | Professional typography, 6 visual themes, theme shop, colorblind support, font scaling, screen shake, particle effects |
| 🏆 **Progression** | 11 achievements, 8 objectives, leaderboard, persistent stats, save/load system |
| ♿ **Accessibility** | 3 colorblind palettes, font scaling, JSON localization, mod support |
| 🔧 **Technical** | State machine architecture, event-driven design, modular systems, PyInstaller packaging |

</div>

### 🎮 Gameplay Features

- **Combo System** - Chain food eats for multiplier bonuses up to **3.0x**
- **Frenzy Mode** - Triggered at 10+ combo for enhanced gameplay
- **Ghost Mode** - Temporary body collision immunity
- **6 Food Types** - Normal, Golden, Poison, Shield, Missile, Ghost
- **Stage Progression** - Dynamic difficulty scaling with obstacle generation
- **AI Opponent** - Advanced pathfinding AI snake

### 🎨 Visual & UI Features

- **Professional UI Framework** - PressStart2P typography, beveled borders, dynamic glow effects
- **6 Visual Themes** - Classic Arcade, Cyberpunk Neon, Retro GameBoy, Golden Mecha, Ghost, The Void
- **Theme Shop** - Collect points to unlock high-rarity skins (Common, Epic, Legendary)
- **Colorblind Support** - Protanopia, Deuteranopia, Tritanopia palettes
- **Font Scaling** - 1.0x to 1.5x for accessibility
- **Screen Shake** - Impact feedback for food, power-ups, and death

### 🏆 Progression Features

- **Achievement System** - 11 achievements including First Blood, Dragon Slayer, Void Walker
- **Objectives System** - 8 objectives with reward points and persistence
- **Leaderboard** - High score tracking with stage information
- **Persistent Stats** - Games played, boss wins, food eaten, max combo
- **Save/Load** - Full game state persistence

---

## 🎮 Game Modes

| Mode | Description | Boss Battles | Timer |
|------|-------------|:---:|:---:|
| **Classic** | The timeless experience with escalating speed | ✅ | ❌ |
| **Time Rush** | Race against the clock - eat food to extend your timer | ❌ | ✅ 60s |
| **Maze Hell** | Start deep in the challenge with advanced stage constraints | ✅ | ❌ |
| **Endless** | Infinite gameplay with no boss battles | ❌ | ❌ |
| **Hardcore** | High-speed mode with boss battles at maximum intensity | ✅ | ❌ |
| **Survival** | Test your endurance in a pure survival challenge | ✅ | ❌ |

---

## 🖼️ Screenshots

<div align="center">

| Main Menu | Theme Shop |
|:---------:|:----------:|
| ![Main Menu](assets/screenshots/main_menu.png) | ![Theme Shop](assets/screenshots/skin_shop.png) |

| Gameplay | Boss Battle |
|:--------:|:-----------:|
| ![Gameplay](assets/screenshots/gameplay.png) | ![Boss Battle](assets/screenshots/boss_battle.png) |

</div>

---

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose | Version |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core Language | 3.11+ |
| ![Pygame](https://img.shields.io/badge/Pygame-green?style=flat-square) | Game Engine | 2.6.1+ |
| ![PyInstaller](https://img.shields.io/badge/PyInstaller-blue?style=flat-square) | Executable Builder | 6.20.0 |
| ![psutil](https://img.shields.io/badge/psutil-orange?style=flat-square) | Process Monitoring | Latest |
| ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white) | CI/CD | Latest |

</div>

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Pip** - Package manager (included with Python)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ZachDreamZ/modular-snake-pro.git
   cd modular-snake-pro
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running from Source

```bash
python src/main.py
```

### Running the Pre-built Executable

1. Download the latest release from [Releases](https://github.com/ZachDreamZ/modular-snake-pro/releases/latest)
2. Extract `SnakeGradient_v0.1.2.exe`
3. Double-click to run

---

## 🎮 Controls

| Key | Action |
|:----|:-------|
| `WASD` / `Arrow Keys` | Move snake |
| `ESC` / `P` | Pause game |
| `Space` | Confirm / Select |
| `Enter` | High score entry confirm |
| `Mouse Click` | Menu navigation |

---

## 🏗️ Architecture

SnakeGradient is built with a modular, state-driven architecture:

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

### Design Principles

- **State Machine Pattern** - Clean separation of game states
- **Event-Driven Architecture** - Reactive event handling
- **Modular Design** - Independent, testable components
- **Configuration-Driven** - All game parameters in `config.py`
- **Separation of Concerns** - UI, logic, and data are decoupled

---

## 🧪 Testing

SnakeGradient includes a comprehensive automated QA testing bot.

### Running Tests

```bash
python -m src.tools.playtest_bot
```

### Test Coverage

The playtest bot performs **50+ automated tests** across these categories:

| Category | Tests | Description |
|----------|:-----:|:------------|
| Audio Pipeline | 1 | Sound loading and playback |
| State Machine | 1 | State transitions (Menu, Shop, Gameplay, Boss) |
| Entity Logic | 4 | Movement, growth, collision, bounce |
| UI System | 2 | Hover effects, shop purchase |
| Boss System | 1 | Boss spawn and state transition |
| v0.0.5 Mechanics | 4 | Combo, ghost, frenzy, void walker |
| v0.0.8 Features | 18 | Achievements, objectives, hints, stats, etc. |
| Behavioral Sims | 9 | Player profiles (Aggressive, Passive, etc.) |
| Edge Cases | 4 | Menu, pause, settings, restart spam |
| Stability | 3 | Long-run, state cycles, save/load stress |
| UX/Accessibility | 6 | First-time, returning, accessibility audit |
| Visual Identity | 2 | Layout validation, visual hierarchy |

### Stress Testing

- **Long-Run Stability**: 300s continuous gameplay (Avg FPS 10.01, Mem Growth 0.43MB)
- **Edge Case Spam**: 500 iterations of menu/pause/settings/restart
- **State Cycle Stress**: 200 game cycles without crash
- **Save/Load Stress**: 1000 save/load cycles without corruption
- **Accessibility Audit**: 48 snapshot combinations

---

## 📦 Building

### Building the Executable

```bash
pyinstaller --onefile ^
  --add-data "assets;assets" ^
  --add-data "localization;localization" ^
  --name SnakeGradient_v0.1.2 ^
  src/main.py
```

### Build Output

```
builds/v0.1.2/
├── executable/
│   └── SnakeGradient_v0.1.2.exe  (21.2MB)
├── assets/
├── logs/
├── build_manifest.md
└── SnakeGradient_v0.1.2.spec
```

---

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

### Latest Release: v0.1.2 (RC2)

- **Player Persona Testing** - 5 distinct personas simulated
- **Real Player Behavior Simulation** - Button spamming, rapid menu switching
- **Edge Case Validation** - Comprehensive boundary testing
- **Boss Battle Pause** - Players can now pause during boss fights
- **Void Theme Accessibility** - All 6 themes properly available in shop

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all public functions
- Write tests for new features

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for the full license text.

---

## 👥 Authors

- **ZachDreamZ** - *Creator, Lead Developer, Game Designer* - [@ZachDreamZ](https://github.com/ZachDreamZ)

See the list of [contributors](CONTRIBUTORS.md) who participated in this project.

---

## 🙏 Acknowledgments

- **Cline** - AI-powered software engineering assistant
- **Pygame Community** - Excellent game development framework
- **All Playtesters** - For valuable feedback during development
- **Open Source Contributors** - Whose libraries made this project possible

---

<div align="center">

### ⭐ Star this repository if you found it useful!

**Made with ❤️ by [ZachDreamZ](https://github.com/ZachDreamZ)**

[⬆ Back to Top](#-snakegradient)

</div>