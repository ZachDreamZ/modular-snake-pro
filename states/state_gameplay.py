import pygame
import random
import math
from config import *
import assets
import ui

class GameplayState:
    def __init__(self):
        pass

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
                        submit_rect = ui.get_text_rect("Press ENTER to Save", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
                        if submit_rect.collidepoint(mx, my):
                            self.save_final_high_score(manager)
                            manager.change_state("MENU")

    def update(self, manager):
        if manager.state == "COUNTDOWN":
            manager.countdown_timer -= 1
            if manager.countdown_timer > 135: manager.countdown_text = "3"
            elif manager.countdown_timer > 90: manager.countdown_text = "2"
            elif manager.countdown_timer > 45: manager.countdown_text = "1"
            elif manager.countdown_timer > 0: manager.countdown_text = "GO!"
            else: manager.change_state("PLAYING")
        elif manager.state == "PLAYING":
            if manager.shield_timer > 0: manager.shield_timer -= 1
            if manager.invulnerability_timer > 0: manager.invulnerability_timer -= 1
            if manager.shield_timer <= 0: manager.snake.has_shield = False
            if manager.current_mode == MODE_TIME_RUSH:
                manager.time_rush_timer -= 1 / manager.game_speed
                manager.survival_timer += 1 / manager.game_speed
                if manager.time_rush_timer <= 0:
                    self.trigger_game_over(manager)
                    return
            head = manager.snake.update()
            manager.ai_snake.update_ai_logic(manager.food.pos)
            ai_head = manager.ai_snake.update()
            collision = False
            if (head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT):
                collision = True
            elif head in manager.snake.body[1:]:
                collision = True
            elif head in manager.ai_snake.body:
                collision = True
            elif head in manager.obstacles:
                collision = True
            if collision:
                if self.handle_collision(manager): return
            if ai_head in manager.snake.body:
                manager.score += 50
                self.reset_ai_snake(manager)
            if head == manager.food.pos: self.handle_food_eat(manager)
            else: manager.snake.pop_tail()
            if ai_head == manager.food.pos: self.handle_ai_food_eat(manager)
            else: manager.ai_snake.pop_tail()
            for p in manager.particles[:]:
                p.update()
                if p.lifetime <= 0: manager.particles.remove(p)
            self.check_achievements(manager)
        elif manager.state == "BOSS_BATTLE":
            self.update_boss_battle(manager)
        elif manager.state == "VICTORY":
            if manager.victory_timer > 0: manager.victory_timer -= 1

    def handle_food_eat(self, manager):
        self.check_achievements(manager)
        if manager.food.type == "normal":
            assets.sound_manager.play("eat")
            manager.score += 10
            if manager.current_mode == MODE_TIME_RUSH: manager.time_rush_timer += 3
        elif manager.food.type == "golden":
            assets.sound_manager.play("powerup")
            manager.score += 30
            manager.snake.body.append(manager.snake.body[-1])
        elif manager.food.type == "poison":
            assets.sound_manager.play("crash")
            manager.score = max(0, manager.score - 20)
            if len(manager.snake.body) > 1: manager.snake.pop_tail()
        elif manager.food.type == "shield":
            assets.sound_manager.play("powerup")
            manager.snake.has_shield = True
            manager.shield_timer = 10 * manager.game_speed
        elif manager.food.type == "missile":
            assets.sound_manager.play("powerup")
            head = manager.snake.body[0]
            manager.projectiles.append(Projectile(head[0] + BLOCK_SIZE//2, head[1] + BLOCK_SIZE//2, manager.snake.direction))
            manager.score += 20
        manager.food_eaten_this_stage += 1
        manager.update_stage()
        self.create_burst(manager, manager.food.pos, manager.theme["food_normal"])
        boss_body = manager.boss.body if manager.boss else None
        manager.food.spawn(manager.snake.body, manager.ai_snake.body, manager.obstacles, boss_body)
        manager.game_speed = min(20, 10 + manager.score // 100)

    def handle_ai_food_eat(self, manager):
        if manager.food.type == "golden": manager.ai_snake.body.append(manager.ai_snake.body[-1])
        elif manager.food.type == "poison" and len(manager.ai_snake.body) > 1: manager.ai_snake.pop_tail()
        self.create_burst(manager, manager.food.pos, COLOR_BLUE)
        manager.food.spawn(manager.snake.body, manager.ai_snake.body, manager.obstacles)

    def reset_ai_snake(self, manager):
        manager.ai_snake = AISnake((BLOCK_SIZE * 15, BLOCK_SIZE * 15))

    def create_burst(self, manager, pos, color, count=10):
        for _ in range(count):
            manager.particles.append(Particle(pos[0], pos[1], color))

    def handle_collision(self, manager):
        if manager.invulnerability_timer > 0: return False
        if manager.snake.has_shield:
            manager.snake.has_shield = False
            manager.shield_timer = 0
            manager.invulnerability_timer = 1 * manager.game_speed
            self.create_burst(manager, manager.snake.body[0], (0, 0, 255))
            return False
        self.create_burst(manager, manager.snake.body[0], COLOR_BOSS_RED, count=30)
        manager.shake_amount = 15
        self.trigger_game_over(manager)
        return True

    def trigger_game_over(self, manager):
        assets.sound_manager.play("crash")
        assets.update_score(manager.score)
        if assets.check_high_score(manager.score): manager.change_state("HIGH_SCORE_ENTRY")
        else: manager.change_state("GAMEOVER")

    def check_achievements(self, manager):
        new_unlocks = []
        if "First Blood" not in manager.unlocked_achievements and manager.score >= 10: new_unlocks.append("First Blood")
        if "Marathon" not in manager.unlocked_achievements and manager.score >= 500: new_unlocks.append("Marathon")
        if "Dragon Slayer" not in manager.unlocked_achievements and manager.state == "VICTORY": new_unlocks.append("Dragon Slayer")
        if "Speed Demon" not in manager.unlocked_achievements and manager.current_mode == MODE_TIME_RUSH and manager.survival_timer >= 120: new_unlocks.append("Speed Demon")
        for ach in new_unlocks:
            manager.unlocked_achievements.append(ach)
            manager.trigger_toast(f"ACHIEVEMENT UNLOCKED: {ach}")
        if new_unlocks: assets.save_achievements(manager.unlocked_achievements)

    def cycle_name_char(self, manager, direction):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        current_char = manager.player_name[manager.name_cursor]
        idx = chars.find(current_char)
        new_idx = (idx + direction) % len(chars)
        manager.player_name[manager.name_cursor] = chars[new_idx]

    def save_final_high_score(self, manager):
        name = "".join(manager.player_name).strip() or "AAA"
        leaderboard = assets.load_leaderboard()
        leaderboard.append({"name": name, "score": manager.score, "stage": manager.stage})
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        assets.save_leaderboard(leaderboard)

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
                self.create_burst(manager, (proj.x, proj.y), COLOR_BOSS_GOLD)
                manager.projectiles.remove(proj)
                if manager.boss.health <= 0: self.trigger_boss_victory(manager)
            elif any(pygame.Rect(seg[0], seg[1], BLOCK_SIZE, BLOCK_SIZE).collidepoint(proj.x, proj.y) for seg in manager.boss.body[1:]):
                manager.boss.health -= 5
                manager.shake_amount = 5
                self.create_burst(manager, (proj.x, proj.y), COLOR_BOSS_RED)
                manager.projectiles.remove(proj)
        if random.random() < 0.02:
            hx = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            hy = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            manager.boss_hazards.append((hx, hy))
            if len(manager.boss_hazards) > 15: manager.boss_hazards.pop(0)
        collision = False
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT): collision = True
        elif head in manager.snake.body[1:]: collision = True
        elif head in manager.boss.body: collision = True
        elif head in manager.boss_hazards: collision = True
        if collision:
            if self.handle_collision(manager): return
        if head == manager.food.pos: self.handle_food_eat(manager)
        else: manager.snake.pop_tail()
        for p in manager.particles[:]:
            p.update()
            if p.lifetime <= 0: manager.particles.remove(p)

    def trigger_boss_victory(self, manager):
        self.check_achievements(manager)
        assets.sound_manager.play("victory")
        manager.score += 1000
        manager.total_points += 1000
        assets.save_total_points(manager.total_points)
        manager.shake_amount = 20
        manager.victory_timer = 120
        manager.change_state("VICTORY")

    def draw(self, manager, offset_x, offset_y):
        if manager.state == "PLAYING" or manager.state == "PAUSED":
            for obs in manager.obstacles:
                pygame.draw.rect(manager.screen, COLOR_GREY, (obs[0] + offset_x, obs[1] + offset_y, BLOCK_SIZE, BLOCK_SIZE))
            manager.food.draw(manager.screen, manager.theme)
            manager.snake.draw(manager.screen)
            manager.ai_snake.draw(manager.screen)
            for p in manager.particles: p.draw(manager.screen)
            ui.draw_text(manager.screen, f"Score: {manager.score}", FONT_SIZE_SMALL, 60, 30, COLOR_WHITE)
            ui.draw_text(manager.screen, f"Stage: {manager.stage}", FONT_SIZE_SMALL, 160, 30, COLOR_WHITE)
            if manager.state == "PAUSED": ui.draw_overlay(manager.screen, "PAUSED", "Press ESC to Resume | Q to Menu")
        
        elif manager.state == "BOSS_BATTLE":
            for hz in manager.boss_hazards:
                pygame.draw.rect(manager.screen, COLOR_PURPLE, (hz[0] + offset_x, hz[1] + offset_y, BLOCK_SIZE, BLOCK_SIZE))
            manager.food.draw(manager.screen, manager.theme)
            manager.snake.draw(manager.screen)
            if manager.boss: manager.boss.draw(manager.screen)
            for proj in manager.projectiles: proj.draw(manager.screen)
            for p in manager.particles: p.draw(manager.screen)
            if manager.boss:
                bar_width, bar_height = 400, 20
                x, y = SCREEN_WIDTH // 2 - bar_width // 2, 20
                pygame.draw.rect(manager.screen, (50, 0, 0), (x, y, bar_width, bar_height))
                health_w = int(bar_width * (manager.boss.health / manager.boss.max_health))
                pygame.draw.rect(manager.screen, COLOR_BOSS_RED, (x, y, health_w, bar_height))
                pygame.draw.rect(manager.screen, COLOR_WHITE, (x, y, bar_width, bar_height), 2)
                ui.draw_text(manager.screen, "MECHA-SNAKE BOSS", FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, y - 15, COLOR_BOSS_GOLD)
            ui.draw_text(manager.screen, f"Score: {manager.score}", FONT_SIZE_SMALL, 60, 30, COLOR_WHITE)
            ui.draw_text(manager.screen, f"Stage: {manager.stage}", FONT_SIZE_SMALL, 160, 30, COLOR_WHITE)
        
        elif manager.state == "GAMEOVER":
            ui.draw_panel(manager.screen, SCREEN_WIDTH // 4, 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            ui.draw_text(manager.screen, "GAME OVER", FONT_SIZE_HUGE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, (255, 0, 0))
            ui.draw_text(manager.screen, f"Final Score: {manager.score}", FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE)
            ui.draw_text(manager.screen, "Press ENTER to Restart | Q for Menu", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, COLOR_WHITE)
        
        elif manager.state == "COUNTDOWN":
            scale_factor = 1.0 + (manager.countdown_timer % 45) / 45 * 0.5
            ui.draw_text(manager.screen, manager.countdown_text, int(FONT_SIZE_HUGE * scale_factor), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE)
        elif manager.state == "HIGH_SCORE_ENTRY":
            self.draw_name_entry(manager)
        elif manager.state == "VICTORY":
            self.draw_victory(manager)

    def draw_victory(self, manager):
        ui.draw_overlay(manager.screen, "VICTORY!", f"Boss Defeated! Bonus 1000 pts\nTotal Score: {manager.score}")
        ui.draw_text(manager.screen, "Press ENTER to return to Menu", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, COLOR_WHITE)

    def draw_name_entry(self, manager):
        ui.draw_text(manager.screen, "NEW HIGH SCORE!", FONT_SIZE_HUGE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, COLOR_YELLOW)
        for i in range(3):
            color = COLOR_YELLOW if i == manager.name_cursor else COLOR_WHITE
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 60 + i * 40, SCREEN_HEIGHT // 2 - 20, 35, 40)
            pygame.draw.rect(manager.screen, color, rect, 2)
            ui.draw_text(manager.screen, manager.player_name[i], FONT_SIZE_MEDIUM, rect.centerx, rect.centery, color)
        ui.draw_text(manager.screen, "Use Arrows/WASD to edit | ENTER to Save", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, COLOR_WHITE)