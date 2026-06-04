import pygame
import random
import math
from config import *
import assets
from entities import Snake, AISnake, Food, Particle, Boss, Projectile

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font, hover_sound=None):
        self.text = text
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.hover_sound = hover_sound
        self.is_hovered = False
        
        # Cache text surface
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                if self.hover_sound:
                    assets.sound_manager.play(self.hover_sound)
                self.is_hovered = True
        else:
            self.is_hovered = False

    def draw(self, surface):
        draw_rect = self.rect
        color = self.color
        
        if self.is_hovered:
            draw_rect = self.rect.inflate(8, 8)
            color = self.hover_color
        
        # Draw button body with rounded corners
        pygame.draw.rect(surface, color, draw_rect, border_radius=12)
        pygame.draw.rect(surface, (0, 0, 0), draw_rect, 3, border_radius=12)
        
        # Draw cached text
        text_rect = self.text_surf.get_rect(center=draw_rect.center)
        surface.blit(self.text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class StateManager:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.state = "MENU"
        self.unlocked_themes = assets.load_unlocked_themes()
        self.theme = THEMES[self.unlocked_themes[0]] if self.unlocked_themes else THEMES["default"]
        self.running = True
        
        # Pre-render background slightly larger for seamless parallax panning
        self.bg_surface = pygame.Surface((SCREEN_WIDTH + BLOCK_SIZE * 2, SCREEN_HEIGHT + BLOCK_SIZE * 2))
        for x in range(0, SCREEN_WIDTH + BLOCK_SIZE * 2, BLOCK_SIZE):
            for y in range(0, SCREEN_HEIGHT + BLOCK_SIZE * 2, BLOCK_SIZE):
                color = COLOR_SLATE_GRAY if (x // BLOCK_SIZE + y // BLOCK_SIZE) % 2 == 0 else COLOR_FOREST_GREEN
                pygame.draw.rect(self.bg_surface, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Shop variables
        self.shop_index = 0
        self.theme_costs = {"default": 0, "dark": 50, "neon": 100, "golden_mecha": 0, "ghost": 0}
        self.theme_keys = ["default", "dark", "neon", "golden_mecha", "ghost"]
        
        # Game specific variables
        self.snake = None
        self.ai_snake = None
        self.food = None
        self.particles = []
        self.score = 0
        self.stage = 1
        self.food_eaten_this_stage = 0
        self.obstacles = []
        self.game_speed = 10
        self.shield_timer = 0
        self.invulnerability_timer = 0
        self.highscore = assets.load_high_score()
        self.total_points = assets.load_total_points()
        
        # Boss Battle variables
        self.boss = None
        self.projectiles = []
        self.boss_hazards = []
        self.shake_amount = 0
        self.victory_timer = 0
        
        # Leaderboard variables
        self.player_name = ["A", "A", "A"]
        self.name_cursor = 0

        # Game Mode variables
        self.current_mode = MODE_CLASSIC
        self.time_rush_timer = 0
        self.survival_timer = 0

        # Settings variables
        self.settings = assets.load_settings()
        assets.sound_manager.set_music(self.settings.get("music", True))
        assets.sound_manager.set_sfx(self.settings.get("sfx", True))

        # Achievement variables
        self.unlocked_achievements = assets.load_achievements()
        self.active_toast = None
        self.toast_timer = 0
        self.toast_offset_y = -50

        # Countdown variables
        self.countdown_timer = 0
        self.countdown_text = ""

        # Menu visual flair
        self.menu_snake = AISnake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Load Premium Font
        try:
            self.pixel_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)
            self.small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
        except Exception as e:
            print(f"Font loading failed: {e}")
            self.pixel_font = pygame.font.SysFont("Arial", 24, bold=True)
            self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
            self.small_font = pygame.font.SysFont("Arial", 12, bold=True)

        # Translucent Menu Canvas
        self.menu_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.menu_overlay.fill((0, 0, 0, 150))
    
        # Premium Menu Buttons (Concept 1 Layout)
        self.menu_buttons = [
            Button("PLAY", SCREEN_WIDTH // 2, 200, 200, 50, (57, 255, 20), (150, 255, 100), self.pixel_font, "click"),
            Button("SHOP", 300, 260, 180, 50, (112, 128, 144), (160, 170, 180), self.pixel_font, "click"),
            Button("SETTINGS", 500, 260, 180, 50, (112, 128, 144), (160, 170, 180), self.pixel_font, "click"),
            Button("LEADERBOARD", SCREEN_WIDTH // 2, 320, 200, 50, (112, 128, 144), (160, 170, 180), self.pixel_font, "click"),
        ]
        
        # Cache static menu text surfaces
        self.title_surf = self.title_font.render("SNAKE GRADIENT", True, COLOR_WHITE)

    def change_state(self, new_state):
        self.state = new_state

    def reset_game(self):
        mode_cfg = GAME_MODES[self.current_mode]
        self.snake = Snake((BLOCK_SIZE * 5, BLOCK_SIZE * 5), self.theme["snake_color"], self.theme["snake_color_dark"])
        self.ai_snake = AISnake((BLOCK_SIZE * 15, BLOCK_SIZE * 15))
        self.food = Food()
        self.stage = mode_cfg["start_stage"]
        self.food_eaten_this_stage = 0
        self.obstacles = []
        
        self.update_stage() 
        
        self.food.spawn(self.snake.body, self.ai_snake.body, self.obstacles)
        self.particles = []
        self.score = 0
        self.game_speed = mode_cfg["base_speed"]
        self.time_rush_timer = mode_cfg["timer"] if mode_cfg["timer"] else 0
        self.survival_timer = 0

    def start_countdown(self):
        self.countdown_timer = 180 # 3 seconds at 60fps
        self.change_state("COUNTDOWN")

    def get_text_rect(self, text, size, x, y):
        font = pygame.font.SysFont("Arial", size, bold=True)
        text_surf = font.render(text, True, (0,0,0))
        return text_surf.get_rect(center=(x, y))

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.state == "MENU":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.change_state("MODE_SELECT")
                    if event.key == pygame.K_s:
                        self.change_state("SHOP")
                    if event.key == pygame.K_o:
                        self.change_state("SETTINGS")
                    if event.key == pygame.K_t:
                        current_idx = self.unlocked_themes.index(next(k for k, v in THEMES.items() if v == self.theme))
                        next_idx = (current_idx + 1) % len(self.unlocked_themes)
                        self.theme = THEMES[self.unlocked_themes[next_idx]]
                    if event.key == pygame.K_l:
                        self.change_state("LEADERBOARD")
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for btn in self.menu_buttons:
                            if btn.is_clicked(mouse_pos):
                                if btn.text == "PLAY": self.change_state("MODE_SELECT")
                                elif btn.text == "SETTINGS": self.change_state("SETTINGS")
                                elif btn.text == "SHOP": self.change_state("SHOP")
                                elif btn.text == "LEADERBOARD": self.change_state("LEADERBOARD")

        elif self.state == "MODE_SELECT":
            self.mode_index = 0 if not hasattr(self, 'mode_index') else self.mode_index
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.mode_index = (self.mode_index - 1) % len(GAME_MODES)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.mode_index = (self.mode_index + 1) % len(GAME_MODES)
                    elif event.key == pygame.K_RETURN:
                        mode_key = list(GAME_MODES.keys())[self.mode_index]
                        self.current_mode = mode_key
                        self.reset_game()
                        self.start_countdown()
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.change_state("MENU")
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        for i in range(len(GAME_MODES)):
                            rect = self.get_text_rect(list(GAME_MODES.values())[i]["name"], 24, SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 3) + i * 60)
                            if rect.collidepoint(mx, my):
                                self.mode_index = i
                                mode_key = list(GAME_MODES.keys())[i]
                                self.current_mode = mode_key
                                self.reset_game()
                                self.start_countdown()

        elif self.state == "PLAYING":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.change_state("PAUSED")
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.snake.direction != (0, BLOCK_SIZE):
                        self.snake.next_direction = (0, -BLOCK_SIZE)
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.snake.direction != (0, -BLOCK_SIZE):
                        self.snake.next_direction = (0, BLOCK_SIZE)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.snake.direction != (BLOCK_SIZE, 0):
                        self.snake.next_direction = (-BLOCK_SIZE, 0)
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.snake.direction != (-BLOCK_SIZE, 0):
                        self.snake.next_direction = (BLOCK_SIZE, 0)

        elif self.state == "PAUSED":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_state("PLAYING")
                    if event.key == pygame.K_q:
                        self.change_state("MENU")

        elif self.state == "GAMEOVER":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.change_state("PLAYING")
                    if event.key == pygame.K_q:
                        self.change_state("MENU")

        elif self.state == "HIGH_SCORE_ENTRY":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.cycle_name_char(-1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.cycle_name_char(1)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.name_cursor = max(0, self.name_cursor - 1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.name_cursor = min(2, self.name_cursor + 1)
                    elif event.key == pygame.K_RETURN:
                        self.save_final_high_score()
                        self.change_state("MENU")
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        for i in range(3):
                            rect = pygame.Rect(SCREEN_WIDTH // 2 - 60 + i * 40, SCREEN_HEIGHT // 2 - 20, 35, 40)
                            if rect.collidepoint(mx, my):
                                self.name_cursor = i
                                self.cycle_name_char(1)
                        submit_rect = self.get_text_rect("Press ENTER to Save", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
                        if submit_rect.collidepoint(mx, my):
                            self.save_final_high_score()
                            self.change_state("MENU")

        elif self.state == "LEADERBOARD":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.change_state("MENU")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        back_rect = self.get_text_rect("Press ESC to Return", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 5 // 6)
                        if back_rect.collidepoint(pygame.mouse.get_pos()):
                            self.change_state("MENU")

        elif self.state == "SETTINGS":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_state("MENU")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        music_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3, 200, 50)
                        if music_rect.collidepoint(mx, my):
                            self.settings["music"] = not self.settings.get("music", True)
                            assets.sound_manager.set_music(self.settings["music"])
                            assets.save_settings(self.settings)
                        sfx_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 80, 200, 50)
                        if sfx_rect.collidepoint(mx, my):
                            self.settings["sfx"] = not self.settings.get("sfx", True)
                            assets.sound_manager.set_sfx(self.settings["sfx"])
                            assets.save_settings(self.settings)

        elif self.state == "SHOP":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_state("MENU")
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.shop_index = (self.shop_index - 1) % len(self.theme_keys)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.shop_index = (self.shop_index + 1) % len(self.theme_keys)
                    elif event.key == pygame.K_b:
                        theme_key = self.theme_keys[self.shop_index]
                        cost = self.theme_costs[theme_key]
                        req_ach = THEMES[theme_key].get("required_achievement")
                        if req_ach and req_ach not in self.unlocked_achievements:
                            self.trigger_toast(f"Locked! Requires: {req_ach}")
                        elif theme_key not in self.unlocked_themes and self.total_points >= cost:
                            self.total_points -= cost
                            assets.save_total_points(self.total_points)
                            self.unlocked_themes.append(theme_key)
                            assets.save_unlocked_themes(self.unlocked_themes)
                    elif event.key == pygame.K_t:
                        theme_key = self.theme_keys[self.shop_index]
                        req_ach = THEMES[theme_key].get("required_achievement")
                        if req_ach and req_ach not in self.unlocked_achievements:
                            self.trigger_toast(f"Locked! Requires: {req_ach}")
                        elif theme_key in self.unlocked_themes:
                            self.theme = THEMES[theme_key]
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        # Grid click handling
                        grid_start_x, grid_start_y = 450, 100
                        card_w, card_h = 120, 80
                        for i, theme_key in enumerate(self.theme_keys):
                            col = i % 2
                            row = i // 2
                            card_rect = pygame.Rect(grid_start_x + col * (card_w + 20), grid_start_y + row * (card_h + 20), card_w, card_h)
                            if card_rect.collidepoint(mx, my):
                                self.shop_index = i
                                # Smart Button Action
                                is_unlocked = theme_key in self.unlocked_themes
                                req_ach = THEMES[theme_key].get("required_achievement")
                                if req_ach and req_ach not in self.unlocked_achievements:
                                    self.trigger_toast(f"Locked! Requires: {req_ach}")
                                elif is_unlocked:
                                    self.theme = THEMES[theme_key]
                                elif self.total_points >= self.theme_costs[theme_key]:
                                    self.total_points -= self.theme_costs[theme_key]
                                    assets.save_total_points(self.total_points)
                                    self.unlocked_themes.append(theme_key)
                                    assets.save_unlocked_themes(self.unlocked_themes)
                                else:
                                    self.trigger_toast("Not enough points!")
                                break
                        # Back button
                        if self.get_text_rect("Press ESC to Return", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 5 // 6).collidepoint(mx, my):
                            self.change_state("MENU")

    def update(self):
        if self.shake_amount > 0:
            self.shake_amount -= 1

        if self.active_toast:
            if self.toast_timer > 0:
                self.toast_timer -= 1
                if self.toast_offset_y < 0:
                    self.toast_offset_y += 2
            else:
                self.toast_offset_y -= 2
                if self.toast_offset_y < -100:
                    self.active_toast = None
                    self.toast_offset_y = -50

        if self.state == "MENU":
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.menu_buttons:
                btn.update(mouse_pos)
        elif self.state == "COUNTDOWN":
            self.countdown_timer -= 1
            if self.countdown_timer > 135: self.countdown_text = "3"
            elif self.countdown_timer > 90: self.countdown_text = "2"
            elif self.countdown_timer > 45: self.countdown_text = "1"
            elif self.countdown_timer > 0: self.countdown_text = "GO!"
            else: self.change_state("PLAYING")
        elif self.state == "PLAYING":
            if self.shield_timer > 0: self.shield_timer -= 1
            if self.invulnerability_timer > 0: self.invulnerability_timer -= 1
            if self.shield_timer <= 0: self.snake.has_shield = False
            if self.current_mode == MODE_TIME_RUSH:
                self.time_rush_timer -= 1 / self.game_speed
                self.survival_timer += 1 / self.game_speed
                if self.time_rush_timer <= 0:
                    self.trigger_game_over()
                    return
            head = self.snake.update()
            self.ai_snake.update_ai_logic(self.food.pos)
            ai_head = self.ai_snake.update()
            collision = False
            if (head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT):
                collision = True
            elif head in self.snake.body[1:]:
                collision = True
            elif head in self.ai_snake.body:
                collision = True
            elif head in self.obstacles:
                collision = True
            if collision:
                if self.handle_collision(): return
            if ai_head in self.snake.body:
                self.score += 50
                self.reset_ai_snake()
            if head == self.food.pos: self.handle_food_eat()
            else: self.snake.pop_tail()
            if ai_head == self.food.pos: self.handle_ai_food_eat()
            else: self.ai_snake.pop_tail()
            for p in self.particles[:]:
                p.update()
                if p.lifetime <= 0: self.particles.remove(p)
            self.check_achievements()
        elif self.state == "BOSS_BATTLE":
            self.update_boss_battle()
        elif self.state == "VICTORY":
            if self.victory_timer > 0: self.victory_timer -= 1
        elif self.state == "PAUSED" or self.state == "GAMEOVER":
            pass

    def handle_food_eat(self):
        self.check_achievements()
        if self.food.type == "normal":
            assets.sound_manager.play("eat")
            self.score += 10
            if self.current_mode == MODE_TIME_RUSH: self.time_rush_timer += 3
        elif self.food.type == "golden":
            assets.sound_manager.play("powerup")
            self.score += 30
            self.snake.body.append(self.snake.body[-1])
        elif self.food.type == "poison":
            assets.sound_manager.play("crash")
            self.score = max(0, self.score - 20)
            if len(self.snake.body) > 1: self.snake.pop_tail()
        elif self.food.type == "shield":
            assets.sound_manager.play("powerup")
            self.snake.has_shield = True
            self.shield_timer = 10 * self.game_speed
        elif self.food.type == "missile":
            assets.sound_manager.play("powerup")
            head = self.snake.body[0]
            self.projectiles.append(Projectile(head[0] + BLOCK_SIZE//2, head[1] + BLOCK_SIZE//2, self.snake.direction))
            self.score += 20
        self.food_eaten_this_stage += 1
        self.update_stage()
        self.create_burst(self.food.pos, self.theme["food_normal"])
        boss_body = self.boss.body if self.boss else None
        self.food.spawn(self.snake.body, self.ai_snake.body, self.obstacles, boss_body)
        self.game_speed = min(20, 10 + self.score // 100)

    def update_stage(self):
        if self.food_eaten_this_stage >= 5:
            self.stage += 1
            self.food_eaten_this_stage = 0
            self.obstacles = []
            if self.stage == 5:
                self.start_boss_battle()
                return
            if self.stage == 2:
                gap_x = SCREEN_WIDTH // 2
                for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
                    if not (gap_x - BLOCK_SIZE <= x <= gap_x):
                        self.obstacles.append((x, SCREEN_HEIGHT // 2))
            elif self.stage >= 3:
                corners = [(0,0), (SCREEN_WIDTH-BLOCK_SIZE,0), (0,SCREEN_HEIGHT-BLOCK_SIZE), (SCREEN_WIDTH-BLOCK_SIZE, SCREEN_HEIGHT-BLOCK_SIZE)]
                for cx, cy in corners:
                    for dx in range(3):
                        for dy in range(3):
                            tx = cx + dx * BLOCK_SIZE if cx == 0 else cx - dx * BLOCK_SIZE
                            ty = cy + dy * BLOCK_SIZE if cy == 0 else cy - dy * BLOCK_SIZE
                            if 0 <= tx < SCREEN_WIDTH and 0 <= ty < SCREEN_HEIGHT:
                                if dx == 0 or dx == 2 or dy == 0 or dy == 2:
                                    self.obstacles.append((tx, ty))

    def handle_ai_food_eat(self):
        if self.food.type == "golden": self.ai_snake.body.append(self.ai_snake.body[-1])
        elif self.food.type == "poison" and len(self.ai_snake.body) > 1: self.ai_snake.pop_tail()
        self.create_burst(self.food.pos, COLOR_BLUE)
        self.food.spawn(self.snake.body, self.ai_snake.body, self.obstacles)

    def reset_ai_snake(self):
        self.ai_snake = AISnake((BLOCK_SIZE * 15, BLOCK_SIZE * 15))

    def create_burst(self, pos, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(pos[0], pos[1], color))

    def handle_collision(self):
        if self.invulnerability_timer > 0: return False
        if self.snake.has_shield:
            self.snake.has_shield = False
            self.shield_timer = 0
            self.invulnerability_timer = 1 * self.game_speed
            self.create_burst(self.snake.body[0], (0, 0, 255))
            return False
        self.create_burst(self.snake.body[0], COLOR_BOSS_RED, count=30)
        self.shake_amount = 15
        self.trigger_game_over()
        return True

    def trigger_game_over(self):
        assets.sound_manager.play("crash")
        assets.update_score(self.score)
        if assets.check_high_score(self.score): self.change_state("HIGH_SCORE_ENTRY")
        else: self.change_state("GAMEOVER")

    def trigger_toast(self, message):
        self.active_toast = message
        self.toast_timer = 180
        self.toast_offset_y = -50

    def check_achievements(self):
        new_unlocks = []
        if "First Blood" not in self.unlocked_achievements and self.score >= 10: new_unlocks.append("First Blood")
        if "Marathon" not in self.unlocked_achievements and self.score >= 500: new_unlocks.append("Marathon")
        if "Dragon Slayer" not in self.unlocked_achievements and self.state == "VICTORY": new_unlocks.append("Dragon Slayer")
        if "Speed Demon" not in self.unlocked_achievements and self.current_mode == MODE_TIME_RUSH and self.survival_timer >= 120: new_unlocks.append("Speed Demon")
        for ach in new_unlocks:
            self.unlocked_achievements.append(ach)
            self.trigger_toast(f"ACHIEVEMENT UNLOCKED: {ach}")
        if new_unlocks: assets.save_achievements(self.unlocked_achievements)

    def cycle_name_char(self, direction):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        current_char = self.player_name[self.name_cursor]
        idx = chars.find(current_char)
        new_idx = (idx + direction) % len(chars)
        self.player_name[self.name_cursor] = chars[new_idx]

    def save_final_high_score(self):
        name = "".join(self.player_name).strip() or "AAA"
        leaderboard = assets.load_leaderboard()
        leaderboard.append({"name": name, "score": self.score, "stage": self.stage})
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        assets.save_leaderboard(leaderboard)

    def draw(self):
        offset_x = random.randint(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        offset_y = random.randint(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        mouse_pos = pygame.mouse.get_pos()
        bg_offset_x = (pygame.time.get_ticks() * 0.02) % BLOCK_SIZE
        bg_offset_y = (pygame.time.get_ticks() * 0.01) % BLOCK_SIZE
        self.screen.blit(self.bg_surface, (offset_x - bg_offset_x, offset_y - bg_offset_y))
        self.screen.blit(self.bg_surface, (offset_x - bg_offset_x + SCREEN_WIDTH, offset_y - bg_offset_y))
        self.screen.blit(self.bg_surface, (offset_x - bg_offset_x, offset_y - bg_offset_y + SCREEN_HEIGHT))
        self.screen.blit(self.bg_surface, (offset_x - bg_offset_x + SCREEN_WIDTH, offset_y - bg_offset_y + SCREEN_HEIGHT))
        
        if self.state == "MENU":
            self.menu_snake.update_ai_logic((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.menu_snake.update()
            self.menu_snake.draw(self.screen)
            self.screen.blit(self.menu_overlay, (0, 0))
            oscillation = int(math.sin(pygame.time.get_ticks() / 300) * 10)
            self.draw_text("SNAKE GRADIENT", 32, SCREEN_WIDTH // 2, 80 + oscillation, COLOR_WHITE, font=self.title_font)
            self.draw_text(f"High Score: {self.highscore}  |  Stage: {self.stage}", 12, SCREEN_WIDTH // 2, 120, COLOR_WHITE, font=self.small_font)
            for btn in self.menu_buttons: btn.draw(self.screen)
        
        elif self.state == "SHOP":
            self.draw_panel(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
            self.draw_text("PREMIUM SKIN SHOP", 48, SCREEN_WIDTH // 2, 80, COLOR_WHITE)
            self.draw_text(f"Wallet: {self.total_points} pts", 18, SCREEN_WIDTH // 2, 120, COLOR_YELLOW)
            
            # Preview Pedestal
            pedestal_x, pedestal_y = 200, 220
            pygame.draw.ellipse(self.screen, (40, 40, 40), (pedestal_x-80, pedestal_y, 160, 60))
            pygame.draw.ellipse(self.screen, (60, 60, 60), (pedestal_x-60, pedestal_y-10, 120, 40))
            
            # Animated Preview Snake
            preview_theme = THEMES[self.theme_keys[self.shop_index]]
            preview_snake = Snake((pedestal_x, pedestal_y), preview_theme["snake_color"], preview_theme["snake_color_dark"])
            # Make it move in a circle
            t = pygame.time.get_ticks() / 500
            preview_snake.body = [(pedestal_x + math.cos(t+i*0.3)*30, pedestal_y + math.sin(t+i*0.3)*20) for i in range(5)]
            preview_snake.draw(self.screen)
            self.draw_text("PREVIEW", 14, pedestal_x, pedestal_y + 70, COLOR_GREY)

            # Skin Grid
            grid_start_x, grid_start_y = 420, 150
            card_w, card_h = 130, 90
            for i, theme_key in enumerate(self.theme_keys):
                col = i % 2
                row = i // 2
                cx = grid_start_x + col * (card_w + 20)
                cy = grid_start_y + row * (card_h + 20)
                rect = pygame.Rect(cx, cy, card_w, card_h)
                
                # Rarity Color
                rarity = THEMES[theme_key].get("rarity", "common")
                border_color = COLOR_RARITY_COMMON if rarity == "common" else COLOR_RARITY_EPIC if rarity == "epic" else COLOR_RARITY_LEGENDARY
                
                # Highlighted card
                bg_color = (60, 60, 60) if i == self.shop_index else (30, 30, 30)
                pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
                pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=10)
                
                # Theme Name
                self.draw_text(THEMES[theme_key]["name"], 14, cx + card_w // 2, cy + 25, COLOR_WHITE)
                
                # Smart Button
                is_unlocked = theme_key in self.unlocked_themes
                is_equipped = self.theme == THEMES[theme_key]
                req_ach = THEMES[theme_key].get("required_achievement")
                
                btn_text = "Equipped" if is_equipped else ("Equip" if is_unlocked else f"{self.theme_costs[theme_key]} pts")
                btn_color = COLOR_GREEN if is_unlocked and not is_equipped else COLOR_GREY if is_equipped else COLOR_YELLOW
                if req_ach and req_ach not in self.unlocked_achievements:
                    btn_text = "🔒 Locked"
                    btn_color = COLOR_SNAKE_DARK if 'COLOR_SNAKE_DARK' in globals() else (50, 50, 50)

                btn_rect = pygame.Rect(cx + 15, cy + 45, card_w - 30, 30)
                pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=5)
                self.draw_text(btn_text, 12, btn_rect.centerx, btn_rect.centery, COLOR_BLACK)

            self.draw_text("S: Back to Menu", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, COLOR_WHITE)
        
        elif self.state == "PLAYING" or self.state == "PAUSED":
            for obs in self.obstacles:
                pygame.draw.rect(self.screen, COLOR_GREY, (obs[0] + offset_x, obs[1] + offset_y, BLOCK_SIZE, BLOCK_SIZE))
            self.food.draw(self.screen, self.theme)
            self.snake.draw(self.screen)
            self.ai_snake.draw(self.screen)
            for p in self.particles: p.draw(self.screen)
            self.draw_text(f"Score: {self.score}", 18, 60, 30, COLOR_WHITE)
            self.draw_text(f"Stage: {self.stage}", 18, 160, 30, COLOR_WHITE)
            if self.state == "PAUSED": self.draw_overlay("PAUSED", "Press ESC to Resume | Q to Menu")

        elif self.state == "BOSS_BATTLE":
            for hz in self.boss_hazards:
                pygame.draw.rect(self.screen, COLOR_PURPLE, (hz[0] + offset_x, hz[1] + offset_y, BLOCK_SIZE, BLOCK_SIZE))
            self.food.draw(self.screen, self.theme)
            self.snake.draw(self.screen)
            if self.boss: self.boss.draw(self.screen)
            for proj in self.projectiles: proj.draw(self.screen)
            for p in self.particles: p.draw(self.screen)
            if self.boss:
                bar_width, bar_height = 400, 20
                x, y = SCREEN_WIDTH // 2 - bar_width // 2, 20
                pygame.draw.rect(self.screen, (50, 0, 0), (x, y, bar_width, bar_height))
                health_w = int(bar_width * (self.boss.health / self.boss.max_health))
                pygame.draw.rect(self.screen, COLOR_BOSS_RED, (x, y, health_w, bar_height))
                pygame.draw.rect(self.screen, COLOR_WHITE, (x, y, bar_width, bar_height), 2)
                self.draw_text("MECHA-SNAKE BOSS", 20, SCREEN_WIDTH // 2, y - 15, COLOR_BOSS_GOLD)
            self.draw_text(f"Score: {self.score}", 18, 60, 30, COLOR_WHITE)
            self.draw_text(f"Stage: {self.stage}", 18, 160, 30, COLOR_WHITE)
        
        elif self.state == "GAMEOVER":
            self.draw_panel(SCREEN_WIDTH // 4, 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            self.draw_text("GAME OVER", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, (255, 0, 0))
            self.draw_text(f"Final Score: {self.score}", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE)
            self.draw_text("Press ENTER to Restart | Q for Menu", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, COLOR_WHITE)
        
        elif self.state == "COUNTDOWN":
            scale_factor = 1.0 + (self.countdown_timer % 45) / 45 * 0.5
            self.draw_text(self.countdown_text, int(64 * scale_factor), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE)
        elif self.state == "HIGH_SCORE_ENTRY":
            self.draw_name_entry()
        elif self.state == "SETTINGS":
            self.draw_panel(SCREEN_WIDTH // 4, 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            self.draw_text("SETTINGS", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6, COLOR_WHITE)
            music_enabled = self.settings.get("music", True)
            music_color = (0, 200, 0) if music_enabled else (200, 0, 0)
            music_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3, 200, 50)
            pygame.draw.rect(self.screen, music_color, music_rect, 2)
            self.draw_text(f"MUSIC: {'ON' if music_enabled else 'OFF'}", 24, SCREEN_WIDTH // 2, music_rect.centery, COLOR_WHITE)
            sfx_enabled = self.settings.get("sfx", True)
            sfx_color = (0, 200, 0) if sfx_enabled else (200, 0, 0)
            sfx_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 80, 200, 50)
            pygame.draw.rect(self.screen, sfx_color, sfx_rect, 2)
            self.draw_text(f"SFX: {'ON' if sfx_enabled else 'OFF'}", 24, SCREEN_WIDTH // 2, sfx_rect.centery, COLOR_WHITE)
            self.draw_text("Press ESC to Return", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 5 // 6, COLOR_WHITE)
        elif self.state == "LEADERBOARD":
            self.draw_panel(SCREEN_WIDTH // 4, 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            self.draw_leaderboard()
        
        if self.active_toast:
            toast_w, toast_h = 300, 50
            tx = SCREEN_WIDTH - toast_w // 2 - 100
            ty = 20 + self.toast_offset_y
            self.draw_panel(tx, ty, toast_w, toast_h, alpha=180)
            self.draw_text(f"🏆 {self.active_toast}", 16, tx + toast_w // 2, ty + toast_h // 2, COLOR_YELLOW)

    def draw_text(self, text, size, x, y, color, font=None):
        if font is None: font = pygame.font.SysFont("Arial", size, bold=True)
        shadow_surf = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(x + 2, y + 2))
        self.screen.blit(shadow_surf, shadow_rect)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)

    def draw_panel(self, x, y, w, h, alpha=150):
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, alpha))
        self.screen.blit(panel, (x, y))

    def draw_overlay(self, title, subtitle):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        self.draw_text(title, 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, COLOR_WHITE)
        self.draw_text(subtitle, 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE)

    def start_boss_battle(self):
        self.change_state("BOSS_BATTLE")
        self.boss = Boss((SCREEN_WIDTH // 2, BLOCK_SIZE))
        self.obstacles = []
        self.boss_hazards = []
        self.projectiles = []
        self.food.spawn(self.snake.body, [], self.obstacles, self.boss.body)

    def update_boss_battle(self):
        head = self.snake.update()
        self.boss.update_ai(head)
        boss_head = self.boss.update()
        for proj in self.projectiles[:]:
            proj.update()
            if proj.x < 0 or proj.x >= SCREEN_WIDTH or proj.y < 0 or proj.y >= SCREEN_HEIGHT:
                self.projectiles.remove(proj)
                continue
            boss_rect = pygame.Rect(self.boss.body[0][0], self.boss.body[0][1], BLOCK_SIZE, BLOCK_SIZE)
            if boss_rect.collidepoint(proj.x, proj.y):
                self.boss.health -= 10
                self.shake_amount = 10
                self.create_burst((proj.x, proj.y), COLOR_BOSS_GOLD)
                self.projectiles.remove(proj)
                if self.boss.health <= 0: self.trigger_boss_victory()
            elif any(pygame.Rect(seg[0], seg[1], BLOCK_SIZE, BLOCK_SIZE).collidepoint(proj.x, proj.y) for seg in self.boss.body[1:]):
                self.boss.health -= 5
                self.shake_amount = 5
                self.create_burst((proj.x, proj.y), COLOR_BOSS_RED)
                self.projectiles.remove(proj)
        if random.random() < 0.02:
            hx = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            hy = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.boss_hazards.append((hx, hy))
            if len(self.boss_hazards) > 15: self.boss_hazards.pop(0)
        collision = False
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT): collision = True
        elif head in self.snake.body[1:]: collision = True
        elif head in self.boss.body: collision = True
        elif head in self.boss_hazards: collision = True
        if collision:
            if self.handle_collision(): return
        if head == self.food.pos: self.handle_food_eat()
        else: self.snake.pop_tail()
        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0: self.particles.remove(p)

    def trigger_boss_victory(self):
        self.check_achievements()
        assets.sound_manager.play("victory")
        self.score += 1000
        self.total_points += 1000
        assets.save_total_points(self.total_points)
        self.shake_amount = 20
        self.victory_timer = 120
        self.change_state("VICTORY")

    def draw_victory(self):
        self.draw_overlay("VICTORY!", f"Boss Defeated! Bonus 1000 pts\nTotal Score: {self.score}")
        self.draw_text("Press ENTER to return to Menu", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, COLOR_WHITE)

    def draw_name_entry(self):
        self.draw_text("NEW HIGH SCORE!", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, COLOR_YELLOW)
        for i in range(3):
            color = COLOR_YELLOW if i == self.name_cursor else COLOR_WHITE
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 60 + i * 40, SCREEN_HEIGHT // 2 - 20, 35, 40)
            pygame.draw.rect(self.screen, color, rect, 2)
            self.draw_text(self.player_name[i], 24, rect.centerx, rect.centery, color)
        self.draw_text("Use Arrows/WASD to edit | ENTER to Save", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, COLOR_WHITE)

    def draw_leaderboard(self):
        self.draw_text("TOP 5 SCORES", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6, COLOR_YELLOW)
        leaderboard = assets.load_leaderboard()
        for i, entry in enumerate(leaderboard):
            text = f"{i+1}. {entry['name']} - Score: {entry['score']} (Stage {entry['stage']})"
            self.draw_text(text, 20, SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 3) + i * 40, COLOR_WHITE)
        if not leaderboard: self.draw_text("No scores yet!", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE)
        self.draw_text("Press ESC to Return", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 5 // 6, COLOR_WHITE)