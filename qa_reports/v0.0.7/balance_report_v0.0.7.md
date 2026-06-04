# Balance Report v0.0.7

## Testing Methodology
- Review of config-based balancing parameters.
- Automated playtest bot verification of combo scoring.
- Manual review of food spawn weights and progression pacing.

## Balancing Parameters

### Food Scores
| Food Type | Base Score | Special Effect |
|-----------|-----------|----------------|
| Normal | 10 | Extends Time Rush timer by 3s |
| Golden | 15 | Grows snake |
| Poison | -20 | Shrinks snake |
| Shield | 0 | Grants shield for 10 game-speed units |
| Missile | 20 | Fires projectile |
| Ghost | 10 | 300-frame ghost mode |

### Combo System
- Multiplier step: every 5 combo = +0.2x
- Max multiplier: 2.0x
- Frenzy threshold: 10 combo
- Combo timer: 60 frames to maintain

### Food Spawn Weights
| Food Type | Weight | Probability |
|-----------|--------|-------------|
| Normal | 50 | 50% |
| Golden | 20 | 20% |
| Poison | 10 | 10% |
| Shield | 8 | 8% |
| Missile | 7 | 7% |
| Ghost | 5 | 5% |

### Difficulty Scaling
- Base speed: 10 (Classic/Maze Hell), 15 (Time Rush)
- Dynamic scaling: `min(20, 10 + sqrt(score/5))`
- Stage progression: Boss at stage 5, mazes at stages 2-4

## Progression Pacing
- **First Blood**: Achievable within first 30 seconds of play.
- **Combo Master**: Requires chaining 10 non-poison food items.
- **Speed Demon**: Requires surviving 120 seconds in Time Rush.
- **Dragon Slayer**: Requires reaching stage 5 and defeating the boss.
- **Void Walker**: Requires surviving 120 seconds in Maze Hell.

## Verdict
- Pacing is appropriate for casual play with skill-based depth.
- Combo system rewards skilled food chaining.
- Difficulty curve is smooth with clear progression gates.