import pygame
import random
import math
from config import *
import game_assets
import ui
from entities import Snake, AISnake, Food, Particle, Boss, Projectile
from localization_manager import loc
from analytics_manager import analytics

class GameplayState:
    def __init__(self):
        self._particle_timer = 0

    def handle_events(self, manager, events):
        if manager.state == "PLAYING":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        manager.change_state("PAUSED")
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and manager.snake.direction != (0, BLOCK_SIZE):
                        manager.snake.next_direction = (0, -BLOCK_SIZE)
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and manager.snake.direction != (0, -BLOCK_SIZE):
                        manager.snake.next_direction = (0, BLOCK_SIZE)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and manager.snake.direction != (BLOCK_SIZE, 0):
                        manager.snake.next_direction = (-BLOCK_SIZE, 0)
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and manager.snake.direction != (-BLOCK_SIZE, 0):
                        manager.snake.next_direction = (BLOCK_SIZE, 0)

        elif manager.state == "PAUSED":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        manager.change_state("PLAYING")
                    if event.key == pygame.K_q:
                        manager.change_state("MENU")

        elif manager.state == "GAMEOVER":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        manager.reset_game()
                        manager.change_state("PLAYING")
                    if event.key == pygame.K_q:
                        manager.change_state("MENU")

        elif manager.state == "HIGH_SCORE_ENTRY":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.cycle_name_char(manager, -1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.cycle_name_char(manager, 1)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        manager.name_cursor = max(0, manager.name_cursor - 1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        manager.name_cursor = min(2, manager.name_cursor + 1)
                    elif event.key == pygame.K_RETURN:
                        self.save_final_high_score(manager)
                        manager.change_state("MENU")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        for i in range(3):
                            rect = pygame.Rect(SCREEN_WIDTH // 2 - 60 + i * 40, SCREEN_HEIGHT // 2 - 20, 35, 40)
                            if rect.collidepoint(mx, my):
                                manager.name_cursor = i
                                self.cycle_name_char(manager, 1)
                        submit_text = loc.get_text("save_hint")
                        submit_rect = ui.get_text_rect(submit_text, FONT_SIZE_SMALL, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
                        if submit_rect.collidepoint(mx, my):
                            self.save_final_high_score(manager)
                            manager.change_state("MENU")

    def update(self, manager):
        if manager.state == "COUNTDOWN":
            manager.countdown_timer -= 1
            if manager.countdown_timer > 135: manager.countdown_text = "3"
            elif manager.countdown_timer > 90: manager.countdown_text = "2"
            elif manager.countdown_timer > 45: manager.countdown_text = "1"
            elif manager.countdown_timer > 0: manager.countdown_text = loc.get_text("countdown_go")
            else:
                manager.change_state("PLAYING")
                if manager.current_mode == MODE_TIME_RUSH:
                    for hint_text, duration in CONTEXTUAL_HINTS.get("time_rush_intro", []):
                        manager.show_contextual_hint(f"rush_{hint_text[:20]}", hint_text, duration)
                elif manager.current_mode == MODE_MAZE_HELL:
                    for hint_text, duration in CONTEXTUAL_HINTS.get("maze_hell_intro", []):
                        manager.show_contextual_hint(f"maze_{hint_text[:20]}", hint_text, duration)
                elif manager.stats.get("games_played", 0) <= 1:
                    for hint_text, duration in CONTEXTUAL_HINTS.get("first_game", []):
                        manager.show_contextual_hint(f"first_{hint_text[:20]}", hint_text, duration)

        elif manager.state == "PLAYING":
            manager.total_game_time += 1
            if manager.shield_timer > 0: manager.shield_timer -= 1
            if manager.invulnerability_timer > 0: manager.invulnerability_timer -= 1
            if manager.ghost_timer > 0: manager.ghost_timer -= 1
            if manager.frenzy_timer > 0: manager.frenzy_timer -= 1
            if manager.combo_timer > 0: manager.combo_timer -= 1
            else: manager.combo_count = 0
            if manager.shield_timer <= 0: manager.snake.has_shield = False
            if manager.current_mode == MODE_TIME_RUSH:
                manager.time_rush_timer -= 1 / manager.game_speed
                manager.survival_timer += 1 / manager.game_speed
                if manager.time_rush_timer <= 0:
                    self.trigger_game_over(manager, "timer")
                    return
            head = manager.snake.update()
            manager.ai_snake.update_ai_logic(manager.food.pos)
            ai_head = manager.ai_snake.update()
            collision = False
            cause = "wall"
            if (head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT):
                collision = True
                cause = "wall"
            elif head in manager.snake.body[1:] and manager.ghost_timer <= 0:
                collision = True
                cause = "self"
            elif head in manager.ai_snake.body:
                collision = True
                cause = "self"
            elif head in manager.obstacles:
                collision = True
                cause = "wall"
            if collision:
                if self.handle_collision(manager, cause): return
            if ai_head in manager.snake.body:
                manager.score += 50
                self.reset_ai_snake(manager)
                self.create_burst(manager, ai_head, COLOR_BLUE, 15)
            if head == manager.food.pos:
                manager.total_food_eaten += 1
                self.handle_food_eat(manager)
            else: manager.snake.pop_tail()
            if ai_head == manager.food.pos: self.handle_ai_food_eat(manager)
            else: manager.ai_snake.pop_tail()
            for p in manager.particles[:]:
                p.update()
                if p.lifetime <= 0: manager.particles.remove(p)
            self._spawn_ambient_particles(manager)
            self.check_achievements(manager)
            self.check_objectives(manager)
        elif manager.state == "BOSS_BATTLE":
            self.update_boss_battle(manager)
        elif manager.state == "VICTORY":
            if manager.victory_timer > 0: manager.victory_timer -= 1

    def _spawn_ambient_particles(self, manager):
        self._particle_timer += 1
        if self._particle_timer > 3:
            self._particle_timer = 0
            if len(manager.particles) < 20:
                cx = random.randint(0, SCREEN_WIDTH)
                cy = random.randint(0, SCREEN_HEIGHT)
                c = (80, 80, 80)
                manager.particles.append(Particle(cx, cy, c, vx=random.uniform(-0.3, 0.3), vy=random.uniform(-0.5, -0.1), size=1, lifetime=60))

    def handle_food_eat(self, manager):
        self.check_achievements(manager)
        self.check_objectives(manager)

        if manager.food.type != "poison":
            manager.combo_count += 1
            manager.combo_timer = 60
            if manager.combo_count >= FRENZY_COMBO_THRESHOLD and manager.frenzy_timer <= 0:
                manager.frenzy_timer = FRENZY_TIMER_DURATION
                manager.trigger_toast(loc.get_text("frenzy_mode"))
        else:
            manager.combo_count = 0

        multiplier = 1.0 + (manager.combo_count // COMBO_MULTIPLIER_STEP) * 0.2
        multiplier = min(multiplier, COMBO_MAX_MULTIPLIER)

        if manager.food.type == "normal":
            game_assets.sound_manager.play("eat")
            manager.score += int(FOOD_SCORES["normal"] * multiplier)
            if manager.current_mode == MODE_TIME_RUSH: manager.time_rush_timer += 3
        elif manager.food.type == "golden":
            game_assets.sound_manager.play("powerup")
            manager.score += int(FOOD_SCORES["golden"] * multiplier)
            manager.snake.body.append(manager.snake.body[-1])
        elif manager.food.type == "poison":
            game_assets.sound_manager.play("crash")
            manager.score = max(0, manager.score + FOOD_SCORES["poison"])
            if len(manager.snake.body) > 1: manager.snake.pop_tail()
        elif manager.food.type == "shield":
            game_assets.sound_manager.play("powerup")
            manager.snake.has_shield = True
            manager.shield_timer = SHIELD_TIMER_UNIT * manager.game_speed
        elif manager.food.type == "missile":
            game_assets.sound_manager.play("powerup")
            head = manager.snake.body[0]
            manager.projectiles.append(Projectile(head[0] + BLOCK_SIZE//2, head[1] + BLOCK_SIZE//2, manager.snake.direction))
            manager.score += int(FOOD_SCORES["missile"] * multiplier)
        elif manager.food.type == "ghost":
            game_assets.sound_manager.play("powerup")
            manager.ghost_timer = GHOST_TIMER_DURATION
            manager.trigger_toast(loc.get_text("ghost_mode"))
            manager.score += int(FOOD_SCORES["ghost"] * multiplier)

        manager.food_eaten_this_stage += 1
        manager.update_stage()
        self.create_burst(manager, manager.food.pos, manager.theme["food_normal"])
        boss_body = manager.boss.body if manager.boss else None
        manager.food.spawn(manager.snake.body, manager.ai_snake.body, manager.obstacles, boss_body)

        manager.game_speed = min(20, 10 + int(math.sqrt(max(0, manager.score / 5))))

    def handle_ai_food_eat(self, manager):
        if manager.food.type == "golden": manager.ai_snake.body.append(manager.ai_snake.body[-1])
        elif manager.food.type == "poison" and len(manager.ai_snake.body) > 1: manager.ai_snake.pop_tail()
        self.create_burst(manager, manager.food.pos, COLOR_BLUE)
        manager.food.spawn(manager.snake.body, manager.ai_snake.body, manager.obstacles)

    def reset_ai_snake(self, manager):
        self.create_burst(manager, manager.ai_snake.body[0], COLOR_BLUE, 20)
        manager.ai_snake = AISnake((BLOCK_SIZE * 15, BLOCK_SIZE * 15))

    def create_burst(self, manager, pos, color, count=10):
        for _ in range(count):
            manager.particles.append(Particle(pos[0], pos[1], color))

    def handle_collision(self, manager, cause):
        if manager.invulnerability_timer > 0: return False
        if manager.snake.has_shield:
            manager.snake.has_shield = False
            manager.shield_timer = 0
            manager.invulnerability_timer = 1 * manager.game_speed
            self.create_burst(manager, manager.snake.body[0], (0, 0, 255), 20)
            return False
        self.create_burst(manager, manager.snake.body[0], COLOR_BOSS_RED, count=30)
        manager.shake_amount = 15
        self.trigger_game_over(manager, cause)
        return True

    def trigger_game_over(self, manager, cause="wall"):
        import save_manager
        game_assets.sound_manager.play("crash")
        save_manager.save_high_score(manager.score)
        analytics.log_game_end(manager.score, cause)
        manager.save_persistent_stats()
        if game_assets.check_high_score(manager.score): manager.change_state("HIGH_SCORE_ENTRY")
        else: manager.change_state("GAMEOVER")

    def check_achievements(self, manager):
        new_unlocks = []
        if "First Blood" not in manager.unlocked_achievements and manager.score >= 10: new_unlocks.append("First Blood")
        if "Marathon" not in manager.unlocked_achievements and manager.score >= 500: new_unlocks.append("Marathon")
        if "Dragon Slayer" not in manager.unlocked_achievements and manager.state == "VICTORY": new_unlocks.append("Dragon Slayer")
        if "Speed Demon" not in manager.unlocked_achievements and manager.current_mode == MODE_TIME_RUSH and manager.survival_timer >= 120: new_unlocks.append("Speed Demon")
        if "Void Walker" not in manager.unlocked_achievements and manager.current_mode == MODE_MAZE_HELL and manager.survival_timer >= 120: new_unlocks.append("Void Walker")
        if "Combo Master" not in manager.unlocked_achievements and manager.combo_count >= 10: new_unlocks.append("Combo Master")
        if "Point Collector" not in manager.unlocked_achievements and manager.stats.get("total_score", 0) + manager.score >= 1000: new_unlocks.append("Point Collector")
        if "Unstoppable" not in manager.unlocked_achievements and manager.boss_wins >= 3: new_unlocks.append("Unstoppable")
        for ach in new_unlocks:
            manager.unlocked_achievements.append(ach)
            manager.trigger_toast(loc.get_text("achievement_unlocked") + ach)
        if new_unlocks: game_assets.save_achievements(manager.unlocked_achievements)

    def check_objectives(self, manager):
        import save_manager
        if "score_100" not in manager.completed_objectives and manager.score >= 100:
            manager.completed_objectives.append("score_100")
            manager.total_points += OBJECTIVE_DEFS["score_100"]["reward"]
            manager.trigger_toast(f"Objective: {OBJECTIVE_DEFS['score_100']['name']} +{OBJECTIVE_DEFS['score_100']['reward']}pts")
        if "score_250" not in manager.completed_objectives and manager.score >= 250:
            manager.completed_objectives.append("score_250")
            manager.total_points += OBJECTIVE_DEFS["score_250"]["reward"]
            manager.trigger_toast(f"Objective: {OBJECTIVE_DEFS['score_250']['name']} +{OBJECTIVE_DEFS['score_250']['reward']}pts")
        if "combo_5" not in manager.completed_objectives and manager.combo_count >= 5:
            manager.completed_objectives.append("combo_5")
            manager.total_points += OBJECTIVE_DEFS["combo_5"]["reward"]
            manager.trigger_toast(f"Objective: {OBJECTIVE_DEFS['combo_5']['name']} +{OBJECTIVE_DEFS['combo_5']['reward']}pts")
        if "eat_50_food" not in manager.completed_objectives and manager.total_food_eaten >= 50:
            manager.completed_objectives.append("eat_50_food")
            manager.total_points += OBJECTIVE_DEFS["eat_50_food"]["reward"]
            manager.trigger_toast(f"Objective: {OBJECTIVE_DEFS['eat_50_food']['name']} +{OBJECTIVE_DEFS['eat_50_food']['reward']}pts")
        if "survive_3_min" not in manager.completed_objectives and manager.total_game_time >= 180 * 10:
            manager.completed_objectives.append("survive_3_min")
            manager.total_points += OBJECTIVE_DEFS["survive_3_min"]["reward"]
            manager.trigger_toast(f"Objective: {OBJECTIVE_DEFS['survive_3_min']['name']} +{OBJECTIVE_DEFS['survive_3_min']['reward']}pts")
        if manager.completed_objectives:
            manager.objectives_progress["completed"] = manager.completed_objectives
            save_manager.save_objectives_progress(manager.objectives_progress)

    def cycle_name_char(self, manager, direction):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        current_char = manager.player_name[manager.name_cursor]
        idx = chars.find(current_char)
        new_idx = (idx + direction) % len(chars)
        manager.player_name[manager.name_cursor] = chars[new_idx]

    def save_final_high_score(self, manager):
        name = "".join(manager.player_name).strip() or "AAA"
        leaderboard = game_assets.load_leaderboard()
        leaderboard.append({"name": name, "score": manager.score, "stage": manager.stage})
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        game_assets.save_leaderboard(leaderboard)

    def update_boss_battle(self, manager):
        head = manager.snake.update()
        manager.boss.update_ai(head)
        boss_head = manager.boss.update()
        for proj in manager.projectiles[:]:
            proj.update()
            if proj.x < 0 or proj.x >= SCREEN_WIDTH or proj.y < 0 or proj.y >= SCREEN_HEIGHT:
                manager.projectiles.remove(proj)
                continue
            boss_rect = pygame.Rect(manager.boss.body[0][0], manager.boss.body[0][1], BLOCK_SIZE, BLOCK_SIZE)
            if boss_rect.collidepoint(proj.x, proj.y):
                manager.boss.health -= 10
                manager.shake_amount = 10
                self.create_burst(manager, (int(proj.x), int(proj.y)), COLOR_BOSS_GOLD, 15)
                manager.projectiles.remove(proj)
                if manager.boss.health <= 0: self.trigger_boss_victory(manager)
            elif any(pygame.Rect(seg[0], seg[1], BLOCK_SIZE, BLOCK_SIZE).collidepoint(proj.x, proj.y) for seg in manager.boss.body[1:]):
                manager.boss.health -= 5
                manager.shake_amount = 5
                self.create_burst(manager, (int(proj.x), int(proj.y)), COLOR_BOSS_RED, 8)
                manager.projectiles.remove(proj)
        if random.random() < 0.02:
            hx = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            hy = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            manager.boss_hazards.append((hx, hy))
            if len(manager.boss_hazards) > 15: manager.boss_hazards.pop(0)
        collision = False
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT): collision = True
        elif head in manager.snake.body[1:] and manager.ghost_timer <= 0: collision = True
        elif head in manager.boss.body: collision = True
        elif head in manager.boss_hazards: collision = True
        if collision:
            if self.handle_collision(manager): return
        if head == manager.food.pos:
            manager.total_food_eaten += 1
            self.handle_food_eat(manager)
        else: manager.snake.pop_tail()
        for p in manager.particles[:]:
            p.update()
            if p.lifetime <= 0: manager.particles.remove(p)

    def trigger_boss_victory(self, manager):
        self.check_achievements(manager)
        self.check_objectives(manager)
        game_assets.sound_manager.play("victory")
        manager.score += 1000
        manager.total_points += 1000
        manager.boss_wins += 1
        game_assets.save_total_points(manager.total_points)
        analytics.log_game_end(manager.score, "victory")
        manager.shake_amount = 20
        manager.victory_timer = 120
        manager.change_state("VICTORY")
        manager.show_contextual_hint("boss_complete", loc.get_text("boss_hint_victory"), 240)

    def draw(self, manager, offset_x, offset_y):
        font_scale = manager.settings.get("font_scale", 1.0)
        settings = manager.settings

        if manager.state == "PLAYING" or manager.state == "PAUSED":
            self._draw_gameplay(manager, offset_x, offset_y, font_scale, settings)
        elif manager.state == "BOSS_BATTLE":
            self._draw_boss_battle(manager, offset_x, offset_y, font_scale, settings)
        elif manager.state == "GAMEOVER":
            self._draw_gameover(manager, font_scale, settings)
        elif manager.state == "COUNTDOWN":
            self._draw_countdown(manager)
        elif manager.state == "HIGH_SCORE_ENTRY":
            self.draw_name_entry(manager)
        elif manager.state == "VICTORY":
            self.draw_victory(manager)

    def _draw_hud_panel(self, manager, font_scale, settings):
        # Top HUD bar - clean glassmorphism
        hud_y = 4
        panel_h = 34
        panel = pygame.Surface((SCREEN_WIDTH, panel_h), pygame.SRCALPHA)
        for x in range(SCREEN_WIDTH):
            alpha = int(80 + 40 * (x / SCREEN_WIDTH))
            pygame.draw.line(panel, (0, 0, 0, alpha), (x, 0), (x, panel_h))
        pygame.draw.line(panel, (255, 255, 255, 30), (0, 0), (SCREEN_WIDTH, 0))
        manager.screen.blit(panel, (0, hud_y))

        y = hud_y + 17
        ui.draw_text(manager.screen, f"{loc.get_text('score_label')}{manager.score}", FONT_SIZE_SMALL, 65, y, COLOR_WHITE, font_multiplier=font_scale, settings=settings)
        ui.draw_text(manager.screen, f"{loc.get_text('stage_label')}{manager.stage}", FONT_SIZE_SMALL, 170, y, (200, 200, 200), font_multiplier=font_scale, settings=settings)

        if manager.current_mode == MODE_TIME_RUSH:
            timer_color = COLOR_RED if manager.time_rush_timer < 10 else COLOR_WHITE
            ui.draw_text(manager.screen, f"{loc.get_text('time_label')}{int(manager.time_rush_timer)}s", FONT_SIZE_SMALL, 280, y, timer_color, font_multiplier=font_scale, settings=settings)

        # Right side - combo/powerups
        rx = SCREEN_WIDTH - 12
        if manager.combo_count > 1:
            combo_color = COLOR_YELLOW if manager.combo_count < 5 else (255, 150, 0) if manager.combo_count < 10 else COLOR_RED
            ui.draw_text(manager.screen, f"{manager.combo_count}x", FONT_SIZE_SMALL, rx, y, combo_color, font_multiplier=font_scale, settings=settings)
            ui.draw_text(manager.screen, "COMBO", FONT_SIZE_TINY, rx - 35, y + 12, combo_color, font_multiplier=font_scale, settings=settings)

        if manager.ghost_timer > 0:
            ghost_pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.5
            c = tuple(int(200 + 55 * ghost_pulse) for _ in range(3))
            ui.draw_text(manager.screen, "GHOST", FONT_SIZE_TINY, rx - 45, y + 12, c, font_multiplier=font_scale, settings=settings)

        if manager.frenzy_timer > 0:
            pulse = (math.sin(pygame.time.get_ticks() * 0.015) + 1) * 0.5
            c = (int(200 + 55 * pulse), 0, 0)
            ui.draw_text(manager.screen, "FRENZY", FONT_SIZE_TINY, rx - 45, y + 12, c, font_multiplier=font_scale, settings=settings)

    def _draw_gameplay(self, manager, offset_x, offset_y, font_scale, settings):
        self._draw_grid_overlay(manager, offset_x, offset_y)
        
        for obs in manager.obstacles:
            pygame.draw.rect(manager.screen, COLOR_GREY, (obs[0] + offset_x, obs[1] + offset_y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(manager.screen, (100, 100, 100), (obs[0] + offset_x + 2, obs[1] + offset_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1)
        manager.food.draw(manager.screen, manager.theme)
        manager.snake.draw(manager.screen)
        manager.ai_snake.draw(manager.screen)
        for p in manager.particles:
            p.draw(manager.screen)

        self._draw_hud_panel(manager, font_scale, settings)

    def _draw_grid_overlay(self, manager, offset_x, offset_y):
        grid_color = (40, 40, 40)
        ox = offset_x % BLOCK_SIZE
        oy = offset_y % BLOCK_SIZE
        for x in range(-ox, SCREEN_WIDTH, BLOCK_SIZE):
            pygame.draw.line(manager.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(-oy, SCREEN_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(manager.screen, grid_color, (0, y), (SCREEN_WIDTH, y))

        if manager.state == "PAUSED":
            ui.draw_overlay(manager.screen, loc.get_text("paused"), loc.get_text("paused_hint"))

    def _draw_boss_battle(self, manager, offset_x, offset_y, font_scale, settings):
        for hz in manager.boss_hazards:
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.3 + 0.7
            c = tuple(int(128 * pulse) for _ in range(3))
            c = (c[0], 0, c[2])
            pygame.draw.rect(manager.screen, c, (hz[0] + offset_x, hz[1] + offset_y, BLOCK_SIZE, BLOCK_SIZE))
        manager.food.draw(manager.screen, manager.theme)
        manager.snake.draw(manager.screen)
        if manager.boss:
            manager.boss.draw(manager.screen)
        for proj in manager.projectiles:
            proj.draw(manager.screen)
        for p in manager.particles:
            p.draw(manager.screen)

        if manager.boss:
            bar_width, bar_height = 350, 16
            x, y = SCREEN_WIDTH // 2 - bar_width // 2, 8
            # Background
            pygame.draw.rect(manager.screen, (30, 0, 0), (x, y, bar_width, bar_height), border_radius=8)
            # Health
            health_w = int(bar_width * (manager.boss.health / manager.boss.max_health))
            if health_w > 0:
                hp_color = COLOR_BOSS_RED if manager.boss.health > 30 else (255, 100, 0)
                pygame.draw.rect(manager.screen, hp_color, (x + 2, y + 2, max(1, health_w - 4), bar_height - 4), border_radius=6)
            # Border
            pygame.draw.rect(manager.screen, COLOR_WHITE, (x, y, bar_width, bar_height), 1, border_radius=8)
            ui.draw_text(manager.screen, f"{loc.get_text('boss_name')} [{manager.boss.health}/{manager.boss.max_health}]", FONT_SIZE_TINY, SCREEN_WIDTH // 2, y + bar_height // 2, COLOR_BOSS_GOLD, font_multiplier=font_scale, settings=settings)

        self._draw_hud_panel(manager, font_scale, settings)

    def _draw_gameover(self, manager, font_scale, settings):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        manager.screen.blit(overlay, (0, 0))

        panel_x, panel_y = SCREEN_WIDTH // 4, 50
        panel_w, panel_h = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100
        ui.draw_panel(manager.screen, panel_x, panel_y, panel_w, panel_h, alpha=180, border_color=COLOR_BOSS_RED)

        ui.draw_glow_text(manager.screen, loc.get_text("game_over"), FONT_SIZE_HUGE, SCREEN_WIDTH // 2, panel_y + 60, (255, 50, 50))
        ui.draw_text(manager.screen, f"{loc.get_text('final_score')}{manager.score}", FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, panel_y + 130, COLOR_WHITE, font_multiplier=font_scale, settings=settings)
        best_score = game_assets.get_high_score()
        ui.draw_text(manager.screen, f"{loc.get_text('best_score')}{best_score}", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, panel_y + 170, COLOR_YELLOW, font_multiplier=font_scale, settings=settings)
        ui.draw_text(manager.screen, loc.get_text("game_over_hint"), FONT_SIZE_SMALL, SCREEN_WIDTH // 2, panel_y + panel_h - 40, COLOR_WHITE, font_multiplier=font_scale, settings=settings)

    def _draw_countdown(self, manager):
        scale_factor = 1.0 + (manager.countdown_timer % 45) / 45 * 0.5
        color = COLOR_GREEN if manager.countdown_text == "GO!" else COLOR_WHITE
        ui.draw_glow_text(manager.screen, manager.countdown_text, int(FONT_SIZE_HUGE * scale_factor), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, color)

    def draw_victory(self, manager):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        manager.screen.blit(overlay, (0, 0))

        ui.draw_glow_text(manager.screen, loc.get_text("victory"), 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, (255, 215, 0))
        ui.draw_text(manager.screen, f"{loc.get_text('victory_msg')}{manager.score}", FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE, font_multiplier=manager.settings.get("font_scale", 1.0), settings=manager.settings)
        ui.draw_text(manager.screen, loc.get_text("victory_hint"), FONT_SIZE_SMALL, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 + 20, COLOR_WHITE, font_multiplier=manager.settings.get("font_scale", 1.0), settings=manager.settings)

        # Particles of victory
        t = pygame.time.get_ticks() / 100
        for i in range(20):
            angle = t + i * math.pi * 2 / 20
            x = SCREEN_WIDTH // 2 + math.cos(angle) * 100
            y = SCREEN_HEIGHT // 3 + math.sin(angle) * 30
            c = (random.randint(200, 255), random.randint(150, 255), random.randint(0, 100))
            pygame.draw.circle(manager.screen, c, (int(x), int(y)), random.randint(2, 5))

    def draw_name_entry(self, manager):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        manager.screen.blit(overlay, (0, 0))

        ui.draw_glow_text(manager.screen, loc.get_text("new_highscore"), FONT_SIZE_HUGE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, COLOR_YELLOW)
        for i in range(3):
            color = COLOR_YELLOW if i == manager.name_cursor else COLOR_WHITE
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 60 + i * 40, SCREEN_HEIGHT // 2 - 20, 35, 40)
            pygame.draw.rect(manager.screen, color, rect, 2)
            ui.draw_text(manager.screen, manager.player_name[i], FONT_SIZE_MEDIUM, rect.centerx, rect.centery, color, font_multiplier=manager.settings.get("font_scale", 1.0), settings=manager.settings)
        ui.draw_text(manager.screen, loc.get_text("highscore_entry_hint"), FONT_SIZE_SMALL, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, COLOR_WHITE, font_multiplier=manager.settings.get("font_scale", 1.0), settings=manager.settings)
