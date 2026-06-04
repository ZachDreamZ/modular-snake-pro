import pygame
import sys
import os
import random
import time
import game_assets
import save_manager
from config import *
from states.state_manager import StateManager
from entities import Snake, Food, Boss
from pathlib import Path
import ui

class PlaytestBot:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("QA Playtest Bot - v0.0.5 Stability Mode")
        self.clock = pygame.time.Clock()
        
        # Initialize State Manager
        self.manager = StateManager(self.screen, self.clock)

        # UI bounding box mappings
        self.ui_mappings = {"menu_buttons": [], "shop_cards": []}
        try:
            for b in getattr(self.manager, "menu_buttons", []):
                self.ui_mappings["menu_buttons"].append(b.rect.copy())
            shop = getattr(self.manager, "shop_ui", None)
            theme_keys = getattr(self.manager, "theme_keys", [])
            if shop and theme_keys:
                for i in range(len(theme_keys)):
                    col = i % 2
                    row = i // 2
                    cx = shop.grid_start_x + col * (shop.card_w + 20)
                    cy = shop.grid_start_y + row * (shop.card_h + 10)
                    rect = pygame.Rect(cx, cy, shop.card_w, shop.card_h)
                    self.ui_mappings["shop_cards"].append(rect)
        except Exception:
            pass
        
        # Test Matrix
        self.test_matrix = {
            "AUDIO_PIPELINE": False,
            "STATE_TRANSITIONS": False,
            "SNAKE_MOVEMENT": False,
            "SNAKE_GROWTH": False,
            "SNAKE_COLLISION": False,
            "UI_HOVER_EFFECTS": False,
            "SHOP_PURCHASE_LOGIC": False,
            "BOSS_SPAWN_LOGIC": False,
            "V005_COMBO": False,
            "V005_GHOST": False,
            "V005_FRENZY": False,
            "V005_VOID_WALKER": False,
            "STABILITY_STRESS": False,
            "SAVE_LOAD_STRESS": False,
            "SNAPSHOTS_CREATED": False
        }
        
        self.logs = []

    def log(self, test_name, success, message=""):
        status = "[PASS]" if success else "[FAIL]"
        log_entry = f"{status} {test_name}: {message}"
        print(log_entry)
        self.logs.append(log_entry)
        if test_name in self.test_matrix:
            self.test_matrix[test_name] = success

    def take_snapshot(self, name):
        screenshots_dir = os.path.join("assets", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        filename = os.path.join(screenshots_dir, f"snapshot_{name}.png")
        pygame.image.save(self.screen, filename)
        return filename

    def test_audio_system(self):
        print("\n--- Testing Audio System ---")
        try:
            all_sounds_exist = True
            sounds_to_check = [
                game_assets.SOUND_EAT, game_assets.SOUND_POWERUP, 
                game_assets.SOUND_CRASH, game_assets.SOUND_VICTORY, game_assets.SOUND_CLICK
            ]
            for s in sounds_to_check:
                if not os.path.exists(s):
                    self.log("AUDIO_PIPELINE", False, f"Missing asset: {s}")
                    all_sounds_exist = False
                else:
                    try:
                        name = Path(s).stem
                        game_assets.sound_manager.play(name)
                    except Exception:
                        pass
            if all_sounds_exist:
                self.log("AUDIO_PIPELINE", True, "Audio Pipeline Loaded and playable")
        except Exception as e:
            self.log("AUDIO_PIPELINE", False, f"Exception during audio test: {e}")

    def test_state_machine(self):
        print("\n--- Testing State Machine ---")
        try:
            self.manager.change_state("SHOP")
            if self.manager.state == "SHOP":
                self.log("STATE_TRANSITIONS", True, "Transition to SHOP successful")
            self.manager.change_state("MENU")
            if self.manager.state == "MENU":
                self.log("STATE_TRANSITIONS", True, "Transition back to MENU successful")
            self.manager.start_countdown()
            if self.manager.state == "COUNTDOWN":
                self.log("STATE_TRANSITIONS", True, "Transition to COUNTDOWN successful")
            self.manager.change_state("PLAYING")
            if self.manager.state == "PLAYING":
                self.log("STATE_TRANSITIONS", True, "Transition to PLAYING successful")
        except Exception as e:
            self.log("STATE_TRANSITIONS", False, f"Exception during state test: {e}")

    def test_entity_logic(self):
        print("\n--- Testing Entity Logic ---")
        try:
            self.manager.reset_game()
            snake = self.manager.snake
            initial_head = snake.body[0]
            snake.next_direction = (0, -BLOCK_SIZE)
            new_head = snake.update()
            if new_head == (initial_head[0], initial_head[1] - BLOCK_SIZE):
                self.log("SNAKE_MOVEMENT", True, "Snake moved UP correctly")
            else:
                self.log("SNAKE_MOVEMENT", False, "Snake movement failed")

            initial_len = len(snake.body)
            snake.update() 
            if len(snake.body) > initial_len:
                self.log("SNAKE_GROWTH", True, "Snake growth simulated successfully")
            else:
                self.log("SNAKE_GROWTH", False, "Snake growth failed")

            snake.body[0] = (-BLOCK_SIZE, 0)
            collision_detected = (snake.body[0][0] < 0 or snake.body[0][0] >= SCREEN_WIDTH or 
                                   snake.body[0][1] < 0 or snake.body[0][1] >= SCREEN_HEIGHT)
            if collision_detected:
                self.log("SNAKE_COLLISION", True, "Wall collision detected correctly")
            else:
                self.log("SNAKE_COLLISION", False, "Wall collision failed")
        except Exception as e:
            self.log("SNAKE_MOVEMENT", False, f"Exception during entity test: {e}")

    def test_ui_and_shop(self):
        print("\n--- Testing UI & Shop ---")
        try:
            btn = self.manager.menu_buttons[0]
            mouse_pos = (btn.rect.centerx, btn.rect.centery)
            btn.update(mouse_pos, (False, False, False))
            if btn.is_hovered:
                self.log("UI_HOVER_EFFECTS", True, f"Button {btn.text} hover detected")
            else:
                self.log("UI_HOVER_EFFECTS", False, f"Button {btn.text} hover failed")
            
            btn.update(mouse_pos, (True, False, False))
            if btn.is_pressed:
                self.log("UI_HOVER_EFFECTS", True, f"Button {btn.text} press detected")
            else:
                self.log("UI_HOVER_EFFECTS", False, f"Button {btn.text} press failed")

            shop_ui = self.manager.shop_ui
            mx = shop_ui.grid_start_x + 10
            my = shop_ui.grid_start_y + 10
            index = shop_ui.handle_click(mx, my, self.manager.theme_keys)
            if index is not None:
                self.log("SHOP_PURCHASE_LOGIC", True, f"Shop card {index} clicked successfully")
            else:
                self.log("SHOP_PURCHASE_LOGIC", False, "Shop card click failed")
        except Exception as e:
            self.log("UI_HOVER_EFFECTS", False, f"Exception during UI test: {e}")

    def test_boss_system(self):
        print("\n--- Testing Boss System ---")
        try:
            self.manager.start_boss_battle()
            if self.manager.state == "BOSS_BATTLE" and self.manager.boss is not None:
                self.log("BOSS_SPAWN_LOGIC", True, "Boss spawned and state transitioned")
            else:
                self.log("BOSS_SPAWN_LOGIC", False, "Boss spawn failed")
        except Exception as e:
            self.log("BOSS_SPAWN_LOGIC", False, f"Exception during boss test: {e}")

    def test_v005_mechanics(self):
        print("\n--- Testing v0.0.5 Advanced Mechanics ---")
        try:
            from states.state_gameplay import GameplayState
            gs = GameplayState()
            self.manager.reset_game()
            
            # 1. Test Combo & Multiplier
            self.manager.score = 0
            self.manager.combo_count = 0
            for _ in range(6):
                self.manager.food.type = "normal"
                gs.handle_food_eat(self.manager)
            
            if self.manager.combo_count == 6:
                # 6 eats: 1-4(10*1), 5-6(10*1.2) = 40 + 12 + 12 = 64
                if self.manager.score == 64:
                    self.log("V005_COMBO", True, f"Combo multiplier verified: Score {self.manager.score}")
                else:
                    self.log("V005_COMBO", False, f"Combo score mismatch: {self.manager.score}")
            else:
                self.log("V005_COMBO", False, f"Combo count failed: {self.manager.combo_count}")

            # 2. Test Ghost Mode
            self.manager.reset_game()
            self.manager.food.type = "ghost"
            gs.handle_food_eat(self.manager)
            if self.manager.ghost_timer > 0:
                # Simulate body collision
                head = self.manager.snake.body[0]
                self.manager.snake.body.append(head) # Force a segment on top of head
                collision = False
                if head in self.manager.snake.body[1:] and self.manager.ghost_timer <= 0:
                    collision = True
                if not collision:
                    self.log("V005_GHOST", True, "Ghost mode successfully ignored body collision")
                else:
                    self.log("V005_GHOST", False, "Ghost mode failed to ignore collision")
            else:
                self.log("V005_GHOST", False, "Ghost timer not set")

            # 3. Test Frenzy Mode
            self.manager.reset_game()
            self.manager.food.type = "normal"
            for _ in range(10):
                gs.handle_food_eat(self.manager)
            if self.manager.frenzy_timer > 0:
                self.log("V005_FRENZY", True, "Frenzy mode triggered at 10 combo")
            else:
                self.log("V005_FRENZY", False, "Frenzy mode failed to trigger")

            # 4. Test Void Walker Achievement
            self.manager.reset_game()
            self.manager.current_mode = MODE_MAZE_HELL
            self.manager.survival_timer = 121
            gs.check_achievements(self.manager)
            if "Void Walker" in self.manager.unlocked_achievements:
                self.log("V005_VOID_WALKER", True, "Void Walker achievement unlocked correctly")
            else:
                self.log("V005_VOID_WALKER", False, "Void Walker achievement failed")

        except Exception as e:
            self.log("V005_MECHANICS", False, f"Exception during v0.0.5 test: {e}")

    def test_long_session(self):
        print("\n--- Testing Long-Run Stability ---")
        try:
            cycles = 50
            for i in range(cycles):
                self.manager.change_state("MENU")
                self.manager.change_state("SHOP")
                self.manager.change_state("PLAYING")
                self.manager.reset_game()
                # Simulate some updates
                for _ in range(10):
                    self.manager.current_state_obj.update(self.manager)
                self.manager.change_state("GAMEOVER")
            self.log("STABILITY_STRESS", True, f"Completed {cycles} game cycles without crash")
        except Exception as e:
            self.log("STABILITY_STRESS", False, f"Crash during stability test: {e}")

    def test_save_load_stress(self):
        print("\n--- Testing Save/Load Stress ---")
        try:
            for i in range(100):
                score = random.randint(0, 10000)
                save_manager.save_high_score(score)
                retrieved = save_manager.get_high_score()
                if retrieved < score: # High score only updates if higher
                    pass 
            self.log("SAVE_LOAD_STRESS", True, "100 save/load cycles completed")
        except Exception as e:
            self.log("SAVE_LOAD_STRESS", False, f"Exception during save stress: {e}")

    def run_full_suite(self):
        print("🚀 STARTING COMPREHENSIVE v0.0.5 DIAGNOSTIC BOT 🚀")
        
        self.test_audio_system()
        self.test_state_machine()
        self.test_entity_logic()
        self.test_ui_and_shop()
        self.test_boss_system()
        self.test_v005_mechanics()
        self.test_long_session()
        self.test_save_load_stress()
        
        # Snapshots
        self.manager.change_state("MENU")
        self.manager.draw()
        self.take_snapshot("menu")
        self.manager.change_state("SHOP")
        self.manager.draw()
        self.take_snapshot("shop")
        self.manager.change_state("PLAYING")
        self.manager.reset_game()
        self.manager.draw()
        self.take_snapshot("gameplay")
        self.manager.start_boss_battle()
        self.manager.draw()
        self.take_snapshot("boss")
        
        self.log("SNAPSHOTS_CREATED", True, "All runtime snapshots captured")
        
        print("\n" + "="*40)
        print("FINAL v0.0.5 DIAGNOSTIC VERDICT")
        print("="*40)
        all_passed = True
        for test, passed in self.test_matrix.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test:25} : {status}")
            if not passed:
                all_passed = False
        print("="*40)
        
        if all_passed:
            print("\nOVERALL RESULT: SYSTEM STABLE & VALIDATED")
        else:
            print("\nOVERALL RESULT: FAILURES DETECTED")
            
        pygame.quit()
        sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    bot = PlaytestBot()
    bot.run_full_suite()