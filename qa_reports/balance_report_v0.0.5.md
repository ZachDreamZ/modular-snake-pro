# Balance Report v0.0.5

## Overview
Version 0.0.5 introduces several balancing changes designed to reward high-skill play and smooth out the difficulty curve for longer sessions.

## Key Changes

### 1. Difficulty Scaling
- **Previous**: Linear speed increase every 50 points.
- **Current**: Non-linear scaling using `10 + sqrt(score / 5)`.
- **Impact**: Speed increases quickly at the start to maintain engagement but plateaus gradually, preventing the game from becoming impossibly fast too early.

### 2. Scoring & Combo System
- **Mechanic**: Introduced a Combo Multiplier that increases every 5 consecutive food eats.
- **Multiplier Formula**: `1.0 + (combo // 5) * 0.2`.
- **Impact**: Players are incentivized to maintain a "streak," making the game more dynamic and rewarding.

### 3. Power-up Balancing
- **Ghost Food**: Provides a 5-second window of body-collision immunity. This is balanced by the fact that it does not increase the snake's length, trading growth for safety.
- **Frenzy Mode**: Triggered at a 10-combo streak. Provides a temporary burst of power and points.

### 4. Progression
- **New Objective**: "Void Walker" requires surviving 120 seconds in Maze Hell mode.
- **New Reward**: "The Void" legendary theme, providing a high-status visual reward for extreme skill.

## Verdict
**BALANCED**