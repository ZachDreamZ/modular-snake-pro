import pygame
import random
import math
from config import *
import game_assets

FOOD_SPRITES = {}

def load_food_sprite(path):
    if path not in FOOD_SPRITES:
        try:
            img = pygame.image.load(path).convert_alpha()
            FOOD_SPRITES[path] = img
        except (pygame.error, FileNotFoundError):
            FOOD_SPRITES[path] = None
    return FOOD_SPRITES[path]

class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, size=None, lifetime=None):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx if vx is not None else random.uniform(-2, 2)
        self.vy = vy if vy is not None else random.uniform(-2, 2)
        self.lifetime = lifetime if lifetime is not None else random.randint(10, 20)
        self.size = size if size is not None else random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # gravity
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = max(0, min(255, int(255 * (self.lifetime / 20))))
            # Ensure color is valid RGB
            base_color = self.color[:3] if len(self.color) >= 3 else (255, 255, 255)
            fc = tuple(max(0, min(255, int(c * self.lifetime / 20))) for c in base_color)
            # Add alpha
            fc = fc + (alpha,)
            s = max(1, int(self.size * (self.lifetime / 20)))
            surf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, fc, (s, s), s)
            surface.blit(surf, (int(self.x - s), int(self.y - s)))

class Food:
    def __init__(self):
        self.pos = (0, 0)
        self.type = "normal"
        self._spawn_time = pygame.time.get_ticks()

    def spawn(self, snake_body, ai_snake_body, obstacles, boss_body=None):
        self._spawn_time = pygame.time.get_ticks()
        while True:
            x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            pos = (x, y)

            on_entity = pos in snake_body or pos in ai_snake_body or pos in obstacles
            if boss_body and pos in boss_body:
                on_entity = True

            if not on_entity:
                rand = random.random()
                if boss_body:
                    if rand < 0.3:
                        self.type = "missile"
                    elif rand < 0.5:
                        self.type = "normal"
                    else:
                        self.type = "golden"
                else:
                    total_weight = sum(FOOD_SPAWN_WEIGHTS.values())
                    roll = random.uniform(0, total_weight)
                    cumulative = 0
                    chosen_type = "normal"
                    for ftype, weight in FOOD_SPAWN_WEIGHTS.items():
                        cumulative += weight
                        if roll <= cumulative:
                            chosen_type = ftype
                            break
                    self.type = chosen_type
                self.pos = pos
                break

    def draw(self, surface, theme):
        cx = self.pos[0] + BLOCK_SIZE // 2
        cy = self.pos[1] + BLOCK_SIZE // 2
        ticks = pygame.time.get_ticks()
        elapsed = ticks - self._spawn_time
        spawn_scale = min(1.0, elapsed / 200)
        bob = math.sin(ticks * 0.006) * 2
        cy_draw = cy + bob

        if self.type == "missile":
            pulse = (math.sin(ticks * 0.01) + 1) * 3
            for r in range(4, 0, -1):
                a = max(0, 60 - r * 12)
                surf = pygame.Surface((BLOCK_SIZE + r * 4, BLOCK_SIZE + r * 4), pygame.SRCALPHA)
                pygame.draw.circle(surf, (0, 255, 255, a), (surf.get_width() // 2, surf.get_height() // 2), BLOCK_SIZE // 2 + r * 2 + pulse)
                surface.blit(surf, (cx - surf.get_width() // 2, cy_draw - surf.get_height() // 2))
            pygame.draw.circle(surface, (0, 255, 255), (cx, int(cy_draw)), int((BLOCK_SIZE // 2 - 1) * spawn_scale))
            pygame.draw.circle(surface, (255, 255, 255), (cx, int(cy_draw)), BLOCK_SIZE // 4)

        elif self.type == "normal":
            size = int((BLOCK_SIZE // 2 - 2) * spawn_scale)
            pygame.draw.circle(surface, (200, 0, 0), (cx, int(cy_draw)), size)
            pygame.draw.circle(surface, (255, 60, 60), (cx - 2, int(cy_draw) - 2), max(1, size - 2))
            stem_pts = [(cx, int(cy_draw) - size), (cx + 2, int(cy_draw) - size - 4)]
            pygame.draw.line(surface, (80, 40, 0), stem_pts[0], stem_pts[1], 2)
            pygame.draw.ellipse(surface, (0, 180, 0), (cx + 2, int(cy_draw) - size - 6, 5, 3))

        elif self.type == "golden":
            pulse = (math.sin(ticks * 0.01) + 1) * 2
            for r in range(3, 0, -1):
                a = max(0, 50 - r * 15)
                surf = pygame.Surface((BLOCK_SIZE + r * 4, BLOCK_SIZE + r * 4), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 215, 0, a), (surf.get_width() // 2, surf.get_height() // 2), BLOCK_SIZE // 2 + r * 2)
                surface.blit(surf, (cx - surf.get_width() // 2, cy_draw - surf.get_height() // 2))
            pygame.draw.circle(surface, (255, 215, 0), (cx, int(cy_draw)), int((BLOCK_SIZE // 2 - 1) * spawn_scale))
            angle = ticks * 0.005
            pts = []
            for i in range(4):
                phi = angle + i * math.pi / 2
                pts.append((cx + math.cos(phi) * 7, cy_draw + math.sin(phi) * 7))
            pygame.draw.polygon(surface, (255, 255, 200), pts)

        elif self.type == "poison":
            sz = int((BLOCK_SIZE // 2 - 2) * spawn_scale)
            pygame.draw.circle(surface, (128, 0, 128), (cx, int(cy_draw)), sz)
            for i in range(8):
                phi = i * math.pi / 4
                p1 = (cx, int(cy_draw))
                p2 = (cx + math.cos(phi) * sz * 1.2, cy_draw + math.sin(phi) * sz * 1.2)
                pygame.draw.line(surface, (180, 50, 180), p1, p2, 2)

        elif self.type == "shield":
            sz = int((BLOCK_SIZE // 2 - 2) * spawn_scale)
            pygame.draw.circle(surface, (0, 100, 255), (cx, int(cy_draw)), sz, 2)
            orb_angle = ticks * 0.007
            ox = cx + math.cos(orb_angle) * sz
            oy = cy_draw + math.sin(orb_angle) * sz
            pygame.draw.circle(surface, (200, 200, 255), (int(ox), int(oy)), 3)

        elif self.type == "ghost":
            sz = int((BLOCK_SIZE // 2 - 1) * spawn_scale)
            for r in range(3, 0, -1):
                a = max(0, 40 - r * 12)
                surf = pygame.Surface((BLOCK_SIZE + r * 4, BLOCK_SIZE + r * 4), pygame.SRCALPHA)
                pygame.draw.circle(surf, (200, 230, 255, a), (surf.get_width() // 2, surf.get_height() // 2), BLOCK_SIZE // 2 + r * 2)
                surface.blit(surf, (cx - surf.get_width() // 2, cy_draw - surf.get_height() // 2))
            pygame.draw.circle(surface, (200, 230, 255), (cx, int(cy_draw)), sz)
            pygame.draw.circle(surface, (220, 240, 255), (cx, int(cy_draw)), max(1, sz // 2))

        else:
            pygame.draw.rect(surface, (255, 255, 255), (self.pos[0], self.pos[1], BLOCK_SIZE, BLOCK_SIZE))

class Snake:
    def __init__(self, start_pos, color, color_dark):
        self.body = [start_pos]
        self.direction = (BLOCK_SIZE, 0)
        self.next_direction = (BLOCK_SIZE, 0)
        self.color = color
        self.color_dark = color_dark
        self.has_shield = False

    def update(self):
        self.direction = self.next_direction
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        return new_head

    def pop_tail(self):
        if len(self.body) > 1:
            self.body.pop()

    def draw(self, surface):
        ticks = pygame.time.get_ticks()

        for i, segment in enumerate(self.body):
            ratio = i / len(self.body) if len(self.body) > 1 else 0
            color = tuple(int(self.color_dark[j] + (self.color[j] - self.color_dark[j]) * ratio) for j in range(3))

            seg_x, seg_y = segment
            cx = seg_x + BLOCK_SIZE // 2
            cy = seg_y + BLOCK_SIZE // 2

            if i == 0:
                # Head glow
                for r in range(4, 0, -1):
                    alpha = 30 // r
                    surf = pygame.Surface((BLOCK_SIZE + r * 8, BLOCK_SIZE + r * 8), pygame.SRCALPHA)
                    pygame.draw.circle(surf, color + (alpha,), (surf.get_width() // 2, surf.get_height() // 2), BLOCK_SIZE // 2 + r * 2)
                    surface.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))

                # Head body
                pygame.draw.circle(surface, color, (cx, cy), BLOCK_SIZE // 2)

                # Highlight
                hl = tuple(min(255, c + 60) for c in color)
                pygame.draw.circle(surface, hl, (cx - 2, cy - 2), BLOCK_SIZE // 4)

                # Directional eyes
                dx, dy = self.direction
                ed = BLOCK_SIZE // 4
                es = BLOCK_SIZE // 7
                perp_x, perp_y = -dy // BLOCK_SIZE, dx // BLOCK_SIZE

                for side in (-1, 1):
                    ex = cx + dx * ed // BLOCK_SIZE + perp_x * ed
                    ey = cy + dy * ed // BLOCK_SIZE + perp_y * ed
                    # Divide properly
                    ex = cx + (dx // BLOCK_SIZE) * ed + perp_x * side * ed // 2
                    ey = cy + (dy // BLOCK_SIZE) * ed + perp_y * side * ed // 2

                    pygame.draw.circle(surface, (255, 255, 255), (int(ex), int(ey)), es)
                    pupil_dx = (dx // BLOCK_SIZE) * es // 3
                    pupil_dy = (dy // BLOCK_SIZE) * es // 3
                    pygame.draw.circle(surface, (0, 0, 0), (int(ex + pupil_dx), int(ey + pupil_dy)), es // 2)

            else:
                # Body segment with smooth connection
                size = BLOCK_SIZE // 2 - 1
                if i < len(self.body) - 1:
                    nxt = self.body[i + 1]
                    angle = math.atan2(segment[1] - nxt[1], segment[0] - nxt[0])
                    dx_c = math.cos(angle) * size
                    dy_c = math.sin(angle) * size
                    # Draw connecting fill between segments
                    pygame.draw.circle(surface, color, (cx, cy), size)
                    # Highlight
                    hl = tuple(min(255, c + 30) for c in color)
                    pygame.draw.circle(surface, hl, (cx - 1, cy - 1), size - 2)

                else:
                    pygame.draw.circle(surface, color, (cx, cy), size)

            # Shield effect
            if self.has_shield and (i == 0 or i % 3 == 0):
                shield_pulse = (math.sin(ticks * 0.01 + i) + 1) * 2
                pygame.draw.circle(surface, (0, 100, 255, 80), (cx, cy), BLOCK_SIZE // 2 + int(shield_pulse), 2)

class AISnake(Snake):
    def __init__(self, start_pos):
        super().__init__(start_pos, COLOR_BLUE, COLOR_DARK_BLUE)

    def update_ai_logic(self, food_pos):
        head = self.body[0]
        dx = food_pos[0] - head[0]
        dy = food_pos[1] - head[1]

        if abs(dx) > abs(dy):
            new_dir = (BLOCK_SIZE if dx > 0 else -BLOCK_SIZE, 0)
        else:
            new_dir = (0, BLOCK_SIZE if dy > 0 else -BLOCK_SIZE)

        self.next_direction = new_dir

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = BLOCK_SIZE * 2
        self.radius = 5
        self._spawn = pygame.time.get_ticks()

    def update(self):
        self.x += self.direction[0] * (self.speed / BLOCK_SIZE)
        self.y += self.direction[1] * (self.speed / BLOCK_SIZE)

    def draw(self, surface):
        ticks = pygame.time.get_ticks()
        elapsed = ticks - self._spawn
        for r in range(3, 0, -1):
            a = max(0, 60 - r * 18)
            surf = pygame.Surface((self.radius * 2 + r * 6, self.radius * 2 + r * 6), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0, 255, 255, a), (surf.get_width() // 2, surf.get_height() // 2), self.radius + r * 2)
            surface.blit(surf, (int(self.x - surf.get_width() // 2), int(self.y - surf.get_height() // 2)))
        pulse = (math.sin(elapsed * 0.02) + 1) * 1.5
        pygame.draw.circle(surface, (0, 255, 255), (int(self.x), int(self.y)), int(self.radius + pulse))

class Boss(Snake):
    def __init__(self, start_pos):
        super().__init__(start_pos, COLOR_BOSS_RED, COLOR_BOSS_GOLD)
        self.max_health = 100
        self.health = self.max_health
        self.body = [start_pos] * 10
        self.direction = (0, BLOCK_SIZE)
        self.target_change_time = pygame.time.get_ticks() + random.randint(1000, 3000)

    def update_ai(self, player_head):
        ticks = pygame.time.get_ticks()
        if ticks > self.target_change_time:
            if random.random() < 0.7:
                dx = player_head[0] - self.body[0][0]
                dy = player_head[1] - self.body[0][1]
                if abs(dx) > abs(dy):
                    self.next_direction = (BLOCK_SIZE if dx > 0 else -BLOCK_SIZE, 0)
                else:
                    self.next_direction = (0, BLOCK_SIZE if dy > 0 else -BLOCK_SIZE)
            else:
                dirs = [(BLOCK_SIZE, 0), (-BLOCK_SIZE, 0), (0, BLOCK_SIZE), (0, -BLOCK_SIZE)]
                self.next_direction = random.choice(dirs)
            self.target_change_time = ticks + random.randint(1000, 3000)

        self.direction = self.next_direction

    def draw(self, surface):
        ticks = pygame.time.get_ticks()
        for i, seg in enumerate(self.body):
            size = BLOCK_SIZE // 2 + 2
            seg_x, seg_y = seg
            cx = seg_x + BLOCK_SIZE // 2
            cy = seg_y + BLOCK_SIZE // 2

            offset_x = math.sin(ticks * 0.005 + i * 0.5) * 4 if i > 0 else 0
            offset_y = math.cos(ticks * 0.005 + i * 0.5) * 4 if i > 0 else 0
            dx, dy = offset_x, offset_y

            base_color = COLOR_BOSS_GOLD if i % 2 == 0 else COLOR_BOSS_RED
            pulse = (math.sin(ticks * 0.008 + i * 0.3) + 1) * 0.15 + 0.7

            color = tuple(max(0, min(255, int(c * pulse))) for c in base_color)

            # Glow
            for r in range(3, 0, -1):
                alpha = 20 // r
                surf = pygame.Surface((BLOCK_SIZE + r * 6, BLOCK_SIZE + r * 6), pygame.SRCALPHA)
                pygame.draw.circle(surf, (220, 20, 60, alpha), (surf.get_width() // 2, surf.get_height() // 2), size + r * 2)
                surface.blit(surf, (int(cx + dx - surf.get_width() // 2), int(cy + dy - surf.get_height() // 2)))

            pygame.draw.circle(surface, color, (int(cx + dx), int(cy + dy)), size)
            pygame.draw.circle(surface, (255, 255, 255), (int(cx + dx), int(cy + dy)), size, 2)

            if i == 0:
                ed = size // 2
                pygame.draw.circle(surface, (255, 200, 0), (int(cx + dx - ed), int(cy + dy - ed)), 4)
                pygame.draw.circle(surface, (255, 200, 0), (int(cx + dx + ed), int(cy + dy - ed)), 4)
