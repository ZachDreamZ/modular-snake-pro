# Snake Gradient - AI Challenge

A modern twist on the classic Snake game with multiple game modes, AI opponents, boss battles, theme shop, achievements, and more.

## Features

- **3 Game Modes**: Classic, Time Rush, Maze Hell
- **AI Opponent**: Compete against an AI snake for food
- **Boss Battles**: Face the Mecha-Snake boss at stage 5
- **Theme Shop**: Unlock and equip visual themes (Neon, GameBoy, Golden Mecha, Ghost)
- **Powerups**: Shield, Missile, Ghost mode, Frenzy mode
- **Combo System**: Chain food eats for score multipliers
- **Achievements & Objectives**: 8 achievements, 5 objectives with rewards
- **Leaderboard**: Track top 5 high scores
- **Localization**: English, Spanish, French
- **Colorblind Accessibility**: 4 colorblind modes
- **Persistent Stats**: Track games played, food eaten, boss wins, and more

## How to Run

### From source:
```
pip install -r requirements.txt
python main.py
```

### Windows executable:
Download the latest release and run `SnakeGradient.exe`

## Controls

| Action | Keys |
|--------|------|
| Move Up | Up Arrow / W |
| Move Down | Down Arrow / S |
| Move Left | Left Arrow / A |
| Move Right | Right Arrow / D |
| Pause | Escape / P |
| Quit to Menu (when paused/game over) | Q |
| Confirm | Enter |

## Game Modes

- **Classic**: Standard snake gameplay. Progress through stages, face the boss at stage 5.
- **Time Rush**: Race against the clock! Eat food to extend your timer.
- **Maze Hell**: Start at stage 4 with complex maze obstacles.

## Building from Source

```
pip install pyinstaller
pyinstaller main.spec
```

The executable will be created in `dist/SnakeGradient/`.

## Installer

Requires [Inno Setup](https://jrsoftware.org/isinfo.php):
```
iscc installer.iss
```
