import pygame
import random
import math
from config import *
import assets

# Asset Cache
FOOD_SPRITES = {}

def load_food_sprite(path):
    if path not in FOOD_SPRITES:
        try:
            img = pygame.image.load(path).convert_alpha()
            FOOD_SPRITES[path] = img
        except (pygame.error, FileNotFoundError):
            print(f"Warning: Could not load sprite {path}")
            FOOD_SPRITES[path] = None
    return FOOD_SPRITES[path]

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.lifetime = random.randint(10, 20)
        self.size = 2

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            # Fade effect by reducing alpha (simulated by darkening)
            alpha_factor = self.lifetime / 20
            fade_color = (
                max(0, min(255, int(self.color[0] * alpha_factor))),
                max(0, min(255, int(self.color[1] * alpha_factor))),
                max(0, min(255, int(self.color[2] * alpha_factor)))
            )
            pygame.draw.rect(surface, fade_color, (int(self.x), int(self.y), self.size, self.size))

class Food:
    def __init__(self):
        self.pos = (0, 0)
        self.type = "normal"

    def spawn(self, snake_body, ai_snake_body, obstacles, boss_body=None):
        while True:
            x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            pos = (x, y)
            
            # Check if spawning on any active entity or obstacle
            on_entity = pos in snake_body or pos in ai_snake_body or pos in obstacles
            if boss_body and pos in boss_body:
                on_entity = True
                
            if not on_entity:
                rand = random.random()
                # Add Missile Fruit for Boss Battle (priority if in Boss Arena)
                if boss_body:
                    if rand < 0.3:
                        self.type = "missile"
                    elif rand < 0.5:
                        self.type = "normal"
                    else:
                        self.type = "golden"
                else:
                    if rand < 0.05:
                        self.type = "shield"
                    elif rand < 0.15:
                        self.type = "golden"
                    elif rand < 0.25:
                        self.type = "poison"
                    else:
                        self.type = "normal"
                self.pos = pos
                break

    def draw(self, surface, theme):
        center = (self.pos[0] + BLOCK_SIZE // 2, self.pos[1] + BLOCK_SIZE // 2)
        ticks = pygame.time.get_ticks()

        if self.type == "missile":
            # Glowing Plasma Apple
            pulse = (math.sin(ticks * 0.01) + 1) * 3
            pygame.draw.circle(surface, COLOR_PLASMA_BLUE, center, BLOCK_SIZE // 2 + pulse, 2)
            pygame.draw.circle(surface, (255, 255, 255), center, BLOCK_SIZE // 4)
        elif self.type == "normal":
            sprite = load_food_sprite("assets/apple.png")
            if sprite:
                # Scale sprite to BLOCK_SIZE
                scaled_sprite = pygame.transform.scale(sprite, (BLOCK_SIZE, BLOCK_SIZE))
                # Blit centered
                surface.blit(scaled_sprite, (self.pos[0], self.pos[1]))
            else:
                # Fallback to crimson circle
                pygame.draw.circle(surface, (200, 0, 0), center, BLOCK_SIZE // 2 - 2)
                pygame.draw.line(surface, (100, 50, 0), center, (center[0], center[1] - BLOCK_SIZE // 2), 2)
                leaf_pt = (center[0] + 3, center[1] - BLOCK_SIZE // 2 - 2)
                pygame.draw.ellipse(surface, (0, 200, 0), (leaf_pt[0]-2, leaf_pt[1]-2, 5, 3))

        elif self.type == "golden":
            # Pulsing outer circle
            pulse = (math.sin(ticks * 0.01) + 1) * 2
            pygame.draw.circle(surface, (255, 255, 0, 100), center, BLOCK_SIZE // 2 + pulse, 1)
            # Rotating Diamond/Star
            angle = ticks * 0.005
            pts = []
            for i in range(4):
                phi = angle + i * math.pi / 2
                pts.append((center[0] + math.cos(phi) * 8, center[1] + math.sin(phi) * 8))
            pygame.draw.polygon(surface, (255, 215, 0), pts)

        elif self.type == "poison":
            # Purple circle with "spikes"
            pygame.draw.circle(surface, (128, 0, 128), center, BLOCK_SIZE // 2 - 2)
            for i in range(8):
                phi = i * math.pi / 4
                p1 = (center[0], center[1])
                p2 = (center[0] + math.cos(phi) * (BLOCK_SIZE // 2 + 2), center[1] + math.sin(phi) * (BLOCK_SIZE // 2 + 2))
                pygame.draw.line(surface, (128, 0, 128), p1, p2, 2)

        elif self.type == "shield":
            # Blue crystal shield
            pygame.draw.circle(surface, (0, 100, 255), center, BLOCK_SIZE // 2 - 2, 2)
            # Orbital particles
            orb_angle = ticks * 0.007
            ox = center[0] + math.cos(orb_angle) * (BLOCK_SIZE // 2)
            oy = center[1] + math.sin(orb_angle) * (BLOCK_SIZE // 2)
            pygame.draw.circle(surface, (200, 200, 255), (int(ox), int(oy)), 2)
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
            # Tapering size
            size = BLOCK_SIZE * (1.0 - (i / len(self.body)) * 0.4) if len(self.body) > 1 else BLOCK_SIZE
            
            # Enhanced organic slither animation
            # Combination of two sine waves for a more fluid, less mechanical movement
            wave1 = math.sin(ticks * 0.008 + i * 0.6) * 3
            wave2 = math.sin(ticks * 0.015 + i * 0.3) * 1.5
            offset_x = (wave1 + wave2) if i > 0 else 0
            offset_y = (math.cos(ticks * 0.008 + i * 0.6) * 2 + math.cos(ticks * 0.015 + i * 0.3) * 1) if i > 0 else 0
            
            pos = (segment[0] + BLOCK_SIZE // 2 + offset_x, segment[1] + BLOCK_SIZE // 2 + offset_y)
            
            # Interpolate color
            ratio = i / len(self.body) if len(self.body) > 1 else 0
            color = tuple(int(self.color_dark[j] + (self.color[j] - self.color_dark[j]) * ratio) for j in range(3))
            
            if i == 0: # Head
                pygame.draw.circle(surface, color, (int(pos[0]), int(pos[1])), int(size // 2))
                
                # Expressive Eyes
                eye_dist = size // 4
                eye_size = size // 6
                
                # Eye offsets based on direction
                # direction is (dx, dy)
                dir_norm = (self.direction[0] / BLOCK_SIZE, self.direction[1] / BLOCK_SIZE)
                
                # Eye positions
                left_eye_pos = (pos[0] - eye_dist, pos[1] - eye_dist)
                right_eye_pos = (pos[0] + eye_dist, pos[1] - eye_dist)
                
                # Draw white of eyes
                pygame.draw.circle(surface, (255, 255, 255), (int(left_eye_pos[0]), int(left_eye_pos[1])), int(eye_size))
                pygame.draw.circle(surface, (255, 255, 255), (int(right_eye_pos[0]), int(right_eye_pos[1])), int(eye_size))
                
                # Draw pupils based on direction
                pupil_offset = ((eye_size // 2) * dir_norm[0], (eye_size // 2) * dir_norm[1])
                pygame.draw.circle(surface, (0, 0, 0), (int(left_eye_pos[0] + pupil_offset[0]), int(left_eye_pos[1] + pupil_offset[1])), int(eye_size // 2))
                pygame.draw.circle(surface, (0, 0, 0), (int(right_eye_pos[0] + pupil_offset[0]), int(right_eye_pos[1] + pupil_offset[1])), int(eye_size // 2))
            else: # Body
                pygame.draw.circle(surface, color, (int(pos[0]), int(pos[1])), int(size // 2))

class AISnake(Snake):
    def __init__(self, start_pos):
        # Using the AI colors from config
        super().__init__(start_pos, COLOR_BLUE, COLOR_DARK_BLUE)

    def update_ai_logic(self, food_pos):
        head = self.body[0]
        dx = food_pos[0] - head[0]
        dy = food_pos[1] - head[1]

        # Decide direction (prioritize larger distance)
        if abs(dx) > abs(dy):
            new_dir = (BLOCK_SIZE if dx > 0 else -BLOCK_SIZE, 0)
        else:
            new_dir = (0, BLOCK_SIZE if dy > 0 else -BLOCK_SIZE)
        
        # Prevent 180-degree turns
        if new_dir != (-self.direction[0], -self.direction[1]):
            self.next_direction = new_dir

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = BLOCK_SIZE * 2
        self.radius = 5

    def update(self):
        self.x += self.direction[0] * (self.speed / BLOCK_SIZE)
        self.y += self.direction[1] * (self.speed / BLOCK_SIZE)

    def draw(self, surface):
        pygame.draw.circle(surface, COLOR_PLASMA_BLUE, (int(self.x), int(self.y)), self.radius)

class Boss(Snake):
    def __init__(self, start_pos):
        super().__init__(start_pos, COLOR_BOSS_RED, COLOR_BOSS_GOLD)
        self.max_health = 100
        self.health = self.max_health
        self.body = [start_pos] * 10 # Start longer
        self.direction = (0, BLOCK_SIZE)
        self.target_change_time = pygame.time.get_ticks() + random.randint(1000, 3000)

    def update_ai(self, player_head):
        ticks = pygame.time.get_ticks()
        if ticks > self.target_change_time:
            # Randomly change direction or chase player
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
        
        # Prevent 180 turns
        if self.next_direction == (-self.direction[0], -self.direction[1]):
            # Just keep moving
            pass
        else:
            self.direction = self.next_direction

    def draw(self, surface):
        ticks = pygame.time.get_ticks()
        for i, segment in enumerate(self.body):
            size = BLOCK_SIZE * 1.2
            # Mecha scale effect: alternate gold and crimson
            color = COLOR_BOSS_GOLD if i % 2 == 0 else COLOR_BOSS_RED
            
            # Boss organic ripple
            offset_x = math.sin(ticks * 0.005 + i * 0.5) * 5 if i > 0 else 0
            offset_y = math.cos(ticks * 0.005 + i * 0.5) * 5 if i > 0 else 0
            
            pos = (segment[0] + BLOCK_SIZE // 2 + offset_x, segment[1] + BLOCK_SIZE // 2 + offset_y)
            
            pygame.draw.circle(surface, color, (int(pos[0]), int(pos[1])), int(size // 2))
            # Add a neon ring
            pygame.draw.circle(surface, (255, 255, 255), (int(pos[0]), int(pos[1])), int(size // 2), 2)
            
            if i == 0: # Boss Head
                # Big menacing eyes
                eye_size = size // 3
                pygame.draw.circle(surface, (255, 255, 0), (int(pos[0] - eye_size), int(pos[1] - eye_size)), 3)
                pygame.draw.circle(surface, (255, 255, 0), (int(pos[0] + eye_size), int(pos[1] - eye_size)), 3)
