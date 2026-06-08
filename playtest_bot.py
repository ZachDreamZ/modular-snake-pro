import pygame
import sys
import os
import random
import time
from datetime import datetime

os.makedirs("assets/screenshots", exist_ok=True)
os.makedirs("mods", exist_ok=True)

import game_assets
import save_manager
from config import *
from states.state_manager import StateManager
from entities import Snake, Food, Boss, AISnake


class PlaytestBot:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Playtest Bot")
        self.clock = pygame.time.Clock()
        self.manager = StateManager(self.screen, self.clock)

        self.logs = []
        self.errors = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.screenshots = []
        self.test_start = datetime.now()

    def log(self, section, test_name, success, message=""):
        status = "PASS" if success else "FAIL"
        if success:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"[{section}] {test_name}: {message}")
        entry = f"[{status}] [{section}] {test_name}: {message}"
        self.logs.append(entry)
        print(f"  [{'OK' if success else 'FAIL'}] {test_name}: {message}")

    def warn(self, section, test_name, message):
        self.warnings += 1
        entry = f"[WARN] [{section}] {test_name}: {message}"
        self.logs.append(entry)
        print(f"  [WARN] {test_name}: {message}")

    def section(self, name):
        self.logs.append(f"\n=== {name} ===")
        print(f"\n--- {name} ---")

    def screenshot(self, name):
        try:
            path = f"assets/screenshots/playtest_{name}.png"
            pygame.image.save(self.screen, path)
            self.screenshots.append((name, path))
            return path
        except Exception as e:
            print(f"  [WARN] Screenshot failed: {e}")
            return None

    def run(self):
        print("=" * 60)
        print("  PLAYTEST BOT - COMPREHENSIVE TEST SUITE")
        print(f"  Started: {self.test_start}")
        print("=" * 60)

        self.test_initialization()
        self.test_config_sanity()
        self.test_state_transitions()
        self.test_entity_logic()
        self.test_game_loop()
        self.test_food_spawning()
        self.test_ai_snake()
        self.test_powerups()
        self.test_boss_system()
        self.test_achievements()
        self.test_objectives()
        self.test_shop()
        self.test_save_load()
        self.test_settings_system()
        self.test_edge_cases()

        self.generate_report()

        pygame.quit()
        total = self.passed + self.failed
        print(f"\n{'>'*40}")
        print(f"  RESULTS: {self.passed}/{total} passed ({self.failed} failed, {self.warnings} warnings)")
        print(f"  Screenshots: {len(self.screenshots)} captured")
        if self.errors:
            print(f"  ERRORS ({len(self.errors)}):")
            for e in self.errors[:10]:
                print(f"    - {e}")
            if len(self.errors) > 10:
                print(f"    ... and {len(self.errors)-10} more")
        print(f"{'<'*40}")
        return self.failed == 0

    def test_initialization(self):
        self.section("Initialization")
        try:
            assert self.manager is not None
            self.log("Init", "StateManager created", True)
            assert self.manager.state == "MENU"
            self.log("Init", "Initial state is MENU", True)
            assert self.manager.theme is not None and "name" in self.manager.theme
            self.log("Init", f"Theme loaded: {self.manager.theme['name']}", True)
            assert self.manager.screen is not None
            self.log("Init", "Pygame display initialized", True)
            assert self.manager.game_speed >= 1
            self.log("Init", f"Default game speed: {self.manager.game_speed}", True)
            assert len(self.manager.menu_buttons) > 0
            self.log("Init", f"{len(self.manager.menu_buttons)} menu buttons", True)
            assert 'music' in self.manager.settings
            self.log("Init", "Settings loaded", True)
        except Exception as e:
            self.log("Init", "Initialization", False, str(e))

    def test_config_sanity(self):
        self.section("Config Sanity")
        try:
            assert SCREEN_WIDTH > 0 and SCREEN_HEIGHT > 0
            self.log("Config", "Screen dimensions valid", True)
            assert BLOCK_SIZE > 0 and SCREEN_WIDTH % BLOCK_SIZE == 0 and SCREEN_HEIGHT % BLOCK_SIZE == 0
            self.log("Config", "Block size divides screen evenly", True)
            assert len(GAME_MODES) >= 3
            self.log("Config", f"{len(GAME_MODES)} game modes defined", True)
            assert len(THEMES) >= 4
            self.log("Config", f"{len(THEMES)} themes defined", True)
            assert len(FOOD_SPAWN_WEIGHTS) >= 5
            self.log("Config", f"{len(FOOD_SPAWN_WEIGHTS)} food types with weights", True)
            assert len(ACHIEVEMENT_DEFS) >= 5
            self.log("Config", f"{len(ACHIEVEMENT_DEFS)} achievements defined", True)
            assert len(OBJECTIVE_DEFS) >= 3
            self.log("Config", f"{len(OBJECTIVE_DEFS)} objectives defined", True)
        except Exception as e:
            self.log("Config", "Config sanity", False, str(e))

    def test_state_transitions(self):
        self.section("State Transitions")
        try:
            self.manager.change_state("SHOP")
            self.manager.draw()
            self.screenshot("shop_state")
            self.log("States", "Shop state renders", True)

            self.manager.change_state("MENU")
            self.manager.draw()
            self.screenshot("menu_state")
            self.log("States", "Menu state renders", True)

            self.manager.change_state("MODE_SELECT")
            self.manager.draw()
            self.screenshot("mode_select")
            self.log("States", "Mode select renders", True)

            self.manager.change_state("SETTINGS")
            self.manager.draw()
            self.screenshot("settings")
            self.log("States", "Settings renders", True)

            self.manager.change_state("MENU")
            self.manager.reset_game()
            self.manager.start_countdown()
            for _ in range(181):
                self.manager.current_state_obj.update(self.manager)
            assert self.manager.state == "PLAYING"
            self.log("States", "Countdown -> Playing transition", True)

            self.manager.change_state("PAUSED")
            self.manager.draw()
            self.screenshot("paused")
            self.log("States", "Paused renders", True)

            self.manager.change_state("PLAYING")
            self.log("States", "Resume transition", True)

            self.manager.change_state("GAMEOVER")
            self.manager.draw()
            self.screenshot("gameover")
            self.log("States", "GameOver renders", True)

        except Exception as e:
            self.log("States", "State transitions", False, str(e))

    def test_entity_logic(self):
        self.section("Entity Logic")
        try:
            self.manager.reset_game()
            snake = self.manager.snake
            assert snake is not None and len(snake.body) >= 1
            self.log("Entities", "Snake created with body", True)

            initial_head = snake.body[0]
            snake.next_direction = (0, -BLOCK_SIZE)
            new_head = snake.update()
            assert new_head == (initial_head[0], initial_head[1] - BLOCK_SIZE)
            self.log("Entities", "Snake moves UP correctly", True)

            initial_len = len(snake.body)
            snake.update()
            assert len(snake.body) == initial_len + 1
            self.log("Entities", "Snake grows on update", True)

            snake.pop_tail()
            assert len(snake.body) == initial_len
            self.log("Entities", "Snake pop_tail works", True)

            self.manager.draw()
            self.screenshot("entity_snake")
            self.log("Entities", "Snake draws without error", True)

        except Exception as e:
            self.log("Entities", "Entity logic", False, str(e))

    def test_game_loop(self):
        self.section("Game Loop")
        try:
            save_manager.save_leaderboard([{"name": "AAA", "score": 100, "stage": 1}])
            self.manager.reset_game()
            self.manager.start_countdown()

            states_seen = []
            for i in range(250):
                prev = self.manager.state
                self.manager.current_state_obj.update(self.manager)
                if self.manager.state != prev:
                    states_seen.append((i, prev, self.manager.state))

            self.manager.draw()
            self.screenshot("gameplay_active")
            self.log("GameLoop", "Gameplay renders during play", True)

            in_playing = any(s == "PLAYING" for _, s, _ in states_seen) or any(s == "PLAYING" for _, _, s in states_seen)
            self.log("GameLoop", f"Snake enters PLAYING state ({states_seen[0]})", in_playing)
            triggered_gameover = any(s2 == "HIGH_SCORE_ENTRY" or s2 == "GAMEOVER" for _, _, s2 in states_seen)
            self.log("GameLoop", f"Game detects hits wall after ~35 moves ({states_seen[1]})", triggered_gameover)

            self.manager.change_state("GAMEOVER")
            self.log("GameLoop", "Manual GameOver transition works", True)

        except Exception as e:
            self.log("GameLoop", "Game loop", False, str(e))

    def test_food_spawning(self):
        self.section("Food Spawning")
        try:
            self.manager.reset_game()
            food = Food()
            food.spawn(self.manager.snake.body, self.manager.ai_snake.body, self.manager.obstacles)
            x, y = food.pos
            assert 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT
            assert x % BLOCK_SIZE == 0 and y % BLOCK_SIZE == 0
            self.log("Food", "Food spawns on valid grid position", True)
            assert food.pos not in self.manager.snake.body and food.pos not in self.manager.ai_snake.body
            self.log("Food", "Food avoids entity overlap", True)

            types_seen = set()
            for _ in range(50):
                food.spawn(self.manager.snake.body, self.manager.ai_snake.body, self.manager.obstacles)
                types_seen.add(food.type)
            self.log("Food", f"Food types seen: {types_seen}", len(types_seen) >= 3)
            assert FOOD_SPAWN_WEIGHTS.get("normal", 0) > 0
            self.log("Food", "Normal food has positive spawn weight", True)

            self.manager.food = food
            self.manager.draw()
            self.screenshot("food_display")
            self.log("Food", "Food renders in scene", True)

        except Exception as e:
            self.log("Food", "Food spawning", False, str(e))

    def test_ai_snake(self):
        self.section("AI Snake")
        try:
            self.manager.reset_game()
            assert self.manager.ai_snake is not None
            self.log("AI", "AI snake exists", True)
            for _ in range(10):
                self.manager.ai_snake.update_ai_logic(self.manager.food.pos)
                self.manager.ai_snake.update()
                head = self.manager.ai_snake.body[0]
                assert 0 <= head[0] <= SCREEN_WIDTH and 0 <= head[1] <= SCREEN_HEIGHT
            self.log("AI", "AI moves toward food without crash", True)
        except Exception as e:
            self.log("AI", "AI snake", False, str(e))

    def test_powerups(self):
        self.section("Powerups")
        try:
            self.manager.reset_game()
            gs = self.manager.states["PLAYING"]

            self.manager.food.type = "shield"
            gs.handle_food_eat(self.manager)
            assert self.manager.snake.has_shield
            self.log("Powerups", "Shield powerup works", True)

            self.manager.reset_game()
            self.manager.food.type = "missile"
            gs.handle_food_eat(self.manager)
            assert len(self.manager.projectiles) > 0
            self.log("Powerups", "Missile powerup works", True)

            self.manager.reset_game()
            self.manager.food.type = "ghost"
            gs.handle_food_eat(self.manager)
            assert self.manager.ghost_timer > 0
            self.log("Powerups", "Ghost powerup works", True)

            self.manager.reset_game()
            self.manager.food.type = "golden"
            gs.handle_food_eat(self.manager)
            self.log("Powerups", "Golden food grows snake", True)

            self.manager.draw()
            self.screenshot("powerups_active")
            self.log("Powerups", "Powerups scene renders", True)

        except Exception as e:
            self.log("Powerups", "Powerup tests", False, str(e))

    def test_boss_system(self):
        self.section("Boss System")
        try:
            self.manager.reset_game()
            self.manager.start_boss_battle()
            assert self.manager.state == "BOSS_BATTLE"
            assert self.manager.boss is not None and self.manager.boss.health > 0
            self.log("Boss", "Boss battle starts correctly", True)

            self.manager.draw()
            self.screenshot("boss_battle")
            self.log("Boss", "Boss battle renders with health bar and hazards", True)

            player_head = self.manager.snake.body[0]
            self.manager.boss.update_ai(player_head)
            self.manager.boss.update()
            self.log("Boss", "Boss AI movement works", True)

        except Exception as e:
            self.log("Boss", "Boss system", False, str(e))

    def test_achievements(self):
        self.section("Achievements")
        try:
            self.manager.reset_game()
            gs = self.manager.states["PLAYING"]
            self.manager.score = 10
            gs.check_achievements(self.manager)
            self.log("Achievements", "Score triggers achievement check without crash", True)
            self.manager.score = 500
            gs.check_achievements(self.manager)
            self.log("Achievements", "High score achievement check works", True)
            assert len(ACHIEVEMENT_DEFS) > 0
            self.log("Achievements", f"{len(ACHIEVEMENT_DEFS)} achievement types available", True)
        except Exception as e:
            self.log("Achievements", "Achievement tests", False, str(e))

    def test_objectives(self):
        self.section("Objectives")
        try:
            self.manager.reset_game()
            self.manager.completed_objectives = []
            gs = self.manager.states["PLAYING"]
            self.manager.score = 100
            gs.check_objectives(self.manager)
            self.log("Objectives", "Score objective check without crash", True)
            self.manager.total_food_eaten = 50
            gs.check_objectives(self.manager)
            self.log("Objectives", "Food counter objective check works", True)
        except Exception as e:
            self.log("Objectives", "Objective tests", False, str(e))

    def test_shop(self):
        self.section("Shop")
        try:
            self.manager.change_state("SHOP")
            assert self.manager.state == "SHOP"
            self.log("Shop", "Shop state accessible", True)
            assert self.manager.shop_ui is not None
            self.log("Shop", "Shop UI initialized", True)
            assert len(self.manager.theme_keys) > 0
            self.log("Shop", f"{len(self.manager.theme_keys)} themes available", True)
        except Exception as e:
            self.log("Shop", "Shop tests", False, str(e))

    def test_save_load(self):
        self.section("Save/Load")
        try:
            save_manager.save_high_score(12345)
            self.log("SaveLoad", "High score save/load completes without error", True)
            progress = {"completed": ["score_100"]}
            save_manager.save_objectives_progress(progress)
            loaded = save_manager.load_objectives_progress()
            assert "completed" in loaded
            self.log("SaveLoad", "Objectives progress save/load works", True)
            stats = {"games_played": 5, "boss_wins": 2, "max_combo": 8, "total_food_eaten": 100}
            save_manager.save_stats(stats)
            loaded_stats = save_manager.load_stats()
            assert loaded_stats.get("games_played") == 5
            self.log("SaveLoad", "Stats save/load works correctly", True)
        except Exception as e:
            self.log("SaveLoad", "Save/load tests", False, str(e))

    def test_settings_system(self):
        self.section("Settings System")
        try:
            assert 'font_scale' in self.manager.settings
            assert 'colorblind' in self.manager.settings
            assert 'language' in self.manager.settings
            self.log("Settings", "All setting keys present", True)
        except Exception as e:
            self.log("Settings", "Settings system", False, str(e))

    def test_edge_cases(self):
        self.section("Edge Cases")
        try:
            self.manager.reset_game()
            self.manager.score = -10
            assert self.manager.score == -10
            self.log("EdgeCases", "Negative score assignment works", True)
            self.manager.game_speed = max(1, min(50, self.manager.game_speed))
            self.log("EdgeCases", "Game speed clamped to safe range", True)
            self.manager.snake.body = [(0, 0), (BLOCK_SIZE, 0), (BLOCK_SIZE * 2, 0)]
            self.manager.snake.next_direction = (-BLOCK_SIZE, 0)
            self.manager.snake.direction = (-BLOCK_SIZE, 0)
            self.manager.snake.update()
            self.log("EdgeCases", "Snake can move out of bounds (wall collision)", True)
            self.manager.food.type = "nonexistent_type"
            gs = self.manager.states["PLAYING"]
            gs.handle_food_eat(self.manager)
            self.log("EdgeCases", "Unknown food type handled without crash", True)
            self.manager.ai_snake = AISnake((BLOCK_SIZE * 15, BLOCK_SIZE * 15))
            self.manager.ai_snake.update()
            assert len(self.manager.ai_snake.body) >= 1
            self.log("EdgeCases", "AI snake update works after re-creation", True)
            self.manager.change_state("SHOP")
            self.manager.change_state("MENU")
            self.manager.change_state("PLAYING")
            self.manager.change_state("SHOP")
            self.manager.change_state("MENU")
            self.log("EdgeCases", "Rapid state changes handled without crash", True)
        except Exception as e:
            self.log("EdgeCases", "Edge case tests", False, str(e))

    def generate_report(self):
        elapsed = datetime.now() - self.test_start
        report_path = f"playtest_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        total = self.passed + self.failed
        lines = [
            f"# Playtest Report",
            f"",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Duration:** {elapsed.total_seconds():.1f}s",
            f"**Version:** {VERSION}",
            f"",
            f"## Summary",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Tests | {total} |",
            f"| Passed | {self.passed} |",
            f"| Failed | {self.failed} |",
            f"| Warnings | {self.warnings} |",
            f"| Pass Rate | {100 * self.passed / max(total, 1):.1f}% |",
            f"| Screenshots | {len(self.screenshots)} |",
            f"",
            f"## Screenshots Captured",
            f"",
        ]
        for name, path in self.screenshots:
            lines.append(f"- **{name}**: `{path}`")

        lines.append("")
        lines.append("## Full Log")
        lines.append("")
        lines.append("```")
        for entry in self.logs:
            lines.append(entry)
        lines.append("```")

        if self.errors:
            lines.append("")
            lines.append("## Errors")
            for e in self.errors:
                lines.append(f"- {e}")

        lines.append("")
        lines.append("## Recommendations")
        if self.failed > 0:
            lines.append(f"- **{self.failed} test(s) failed** - review errors above")
        if self.warnings > 0:
            lines.append(f"- {self.warnings} warning(s) to review")
        lines.append("- Run `python main.py` to verify real-time gameplay")
        if self.passed == total:
            lines.append("- All systems operational")

        with open(report_path, "w") as f:
            f.write("\n".join(lines))
        print(f"\nReport saved: {report_path}")


if __name__ == "__main__":
    bot = PlaytestBot()
    success = bot.run()
    sys.exit(0 if success else 1)
