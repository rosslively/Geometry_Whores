import random
import pygame
import math
from enemy import BlueEnemy, RedEnemy,  YellowEnemy, PurpleEnemy, GreenEnemy, TankEnemy
from assets import Assets
assets = Assets.load_assets()
spawn_sound = assets["spawn_sound"]
clock = pygame.time.Clock()

class SpawnManager:
    def __init__(self, enemies, spawn_area, waves=None):
        self.enemies = enemies
        self.finished = False
        self.spawn_area = spawn_area
        if waves is None:
            waves = [
    {"time": 1, "enemies": [RedEnemy]*8},
    {"time": 1, "enemies": [RedEnemy]*15},
    {"time": 1, "enemies": [BlueEnemy]*18},
    {"time": 1, "enemies": [RedEnemy]*26},
    {"time": 1, "enemies": [spawn_random_enemy(exclude=[PurpleEnemy])] * 12},
    {"time": 1, "enemies": [RedEnemy]*30},
    {"time": 1, "enemies": [spawn_random_enemy(exclude=[RedEnemy, PurpleEnemy])] * 20},
    {"time": 1, "enemies": [RedEnemy]*28},
    {"time": 1, "enemies": [spawn_random_enemy(exclude=[RedEnemy])] * 12},
    {"time": 1, "enemies": [BlueEnemy]*20},
    {"time": 1, "enemies": [spawn_random_enemy(exclude=[RedEnemy])] * 11},
    {"time": 1, "enemies": [TankEnemy]*1},
    {"time": 1, "enemies": [RedEnemy]*40},
    {"time": 1, "enemies": [spawn_random_enemy(exclude=[RedEnemy])] * 9},
    {"time": 1, "enemies": [RedEnemy]*33},
    {"time": 1, "enemies": [RedEnemy]*37},
    {"time": 1, "enemies": [spawn_random_enemy(exclude=[RedEnemy])] * 10},
    {"time": 1, "enemies": [GreenEnemy]*15},
    {"time": 1, "enemies": [RedEnemy]*34},
    {"time": 1, "enemies": [RedEnemy]*40},
    {"time": 1, "enemies": [BlueEnemy]*30},
    {"time": 1, "enemies": [TankEnemy]*2},
    {"time": 1, "enemies": [GreenEnemy]*22},
    {"time": 1, "enemies": [RedEnemy]*24 + [spawn_random_enemy(exclude=[RedEnemy])] * 12},
    {"time": 1, "enemies": [PurpleEnemy]*6},
    {"time": 1, "enemies": [RedEnemy]*36},
    {"time": 1, "enemies": [YellowEnemy]*9 + [BlueEnemy]*9},
    {"time": 1, "enemies": [GreenEnemy]*12 + [RedEnemy]*12},
    {"time": 1, "enemies": [PurpleEnemy]*9},
    {"time": 1, "enemies": [YellowEnemy]*18},
    {"time": 1, "enemies": [BlueEnemy]*9 + [GreenEnemy]*9},
    {"time": 8, "enemies": [RedEnemy]*30 + [PurpleEnemy]*6},
    {"time": 5, "enemies": [BlueEnemy, GreenEnemy, PurpleEnemy]*10},
    {"time": 6, "enemies": [BlueEnemy]*24 + [RedEnemy]*24},
    {"time": 4, "enemies": [TankEnemy]*1 + [RedEnemy] * 10},
    {"time": 6, "enemies": [YellowEnemy]*18 + [GreenEnemy]*12},
    {"time": 5, "enemies": [PurpleEnemy]*9 + [RedEnemy]*36},
    {"time": 5, "enemies": [BlueEnemy]*30 + [YellowEnemy]*15},
    {"time": 4, "enemies": [GreenEnemy]*24 + [RedEnemy]*42 + [YellowEnemy]*15},
    {"time": 4, "enemies": [PurpleEnemy]*30 + [GreenEnemy]*30},
    {"time": 3, "enemies": [BlueEnemy, RedEnemy, YellowEnemy,]*20},
    {"time": 3, "enemies": [RedEnemy]*45 + [YellowEnemy]*30},
    {"time": 2, "enemies": [PurpleEnemy]*60 + [GreenEnemy]*30},
    {"time": 2, "enemies": [RedEnemy, YellowEnemy, GreenEnemy]*30},
    {"time": 1, "enemies": [YellowEnemy, GreenEnemy, PurpleEnemy]*40},
    {"time": 1, "enemies": [RedEnemy]*150},
    {"time": 1, "enemies": [PurpleEnemy]*120},
    {"time": 1, "enemies": [GreenEnemy]*300},
    {"time": 1, "enemies": [BlueEnemy, YellowEnemy, GreenEnemy, PurpleEnemy]*150},

]
        self.waves = waves
        self.current_wave = 0
        self.wave_start_time = pygame.time.get_ticks()
        self.cluster_size = 1
        self.max_spawn_attempts = 10
        self.collision_push_strength = 1

    def update(self, screen_width, screen_height):
        dt = clock.tick(60)

        if self.current_wave < len(self.waves):
            if not self.enemies:  # Wait until current enemies are cleared
                now = pygame.time.get_ticks()
                if now - self.wave_start_time > self.waves[self.current_wave]["time"] * 1000:
                    wave = self.waves[self.current_wave]
                    self.choose_random_spawn_area(screen_width, screen_height)
                    self.spawn_wave(wave)
                    self.current_wave += 1
                    spawn_sound.play()
                    self.wave_start_time = now  # Reset timer for next wait
        self.avoid_enemy_collisions(dt)
        if self.current_wave >= len(self.waves) and not self.enemies:
            self.finished = True

    def spawn_wave(self, wave):
        for EnemyClass in wave["enemies"]:

            base_x = random.randint(self.spawn_area.left, self.spawn_area.right)
            base_y = random.randint(self.spawn_area.top, self.spawn_area.bottom)


            for _ in range(self.cluster_size):
                offset_x = random.randint(-20, 20)
                offset_y = random.randint(-20, 20)
                spawn_x = base_x + offset_x
                spawn_y = base_y + offset_y

                self.spawn_enemy_non_overlapping(EnemyClass, (spawn_x, spawn_y))

    def spawn_enemy_non_overlapping(self, EnemyClass, pos):
        attempts = 0
        while attempts < self.max_spawn_attempts:
            enemy = EnemyClass(pos)


            if not any(enemy.rect.colliderect(e.rect) for e in self.enemies):
                self.enemies.append(enemy)
                return
            else:

                pos = (
                    pos[0] + random.randint(-15, 15),
                    pos[1] + random.randint(-15, 15),
                )
                attempts += 1

        enemy = EnemyClass(pos)
        self.enemies.append(enemy)

    def avoid_enemy_collisions(self, dt):
        for i in range(len(self.enemies)):
            for j in range(i + 1, len(self.enemies)):
                e1 = self.enemies[i]
                e2 = self.enemies[j]
                offset = (e2.rect.left - e1.rect.left, e2.rect.top - e1.rect.top)

                if e1.mask.overlap(e2.mask, offset):
                    dx = e1.pos_x - e2.pos_x
                    dy = e1.pos_y - e2.pos_y
                    dist = math.hypot(dx, dy)

                    if dist == 0:
                        dx, dy = 0.1, 0.1
                        dist = math.hypot(dx, dy)

                    nx = dx / dist
                    ny = dy / dist

                    push_strength = self.collision_push_strength * 800
                    push_distance = min(push_strength * (dt / 1000), 1.3)  # Cap movement

                    push_x = nx * push_distance
                    push_y = ny * push_distance

                    damping = 0.7
                    e1.pos_x += push_x * damping
                    e1.pos_y += push_y * damping
                    e2.pos_x -= push_x * damping
                    e2.pos_y -= push_y * damping

                    e1.rect.centerx = int(e1.pos_x)
                    e1.rect.centery = int(e1.pos_y)
                    e2.rect.centerx = int(e2.pos_x)
                    e2.rect.centery = int(e2.pos_y)


    def choose_random_spawn_area(self, screen_width, screen_height):
        min_width, max_width = 10, 20
        min_height, max_height = 10, 20

        width = random.randint(min_width, max_width)
        height = random.randint(min_height, max_height)

        x = random.randint(0, max(0, screen_width - width))
        y = random.randint(0, max(0, screen_height - height))

        self.spawn_area = pygame.Rect(x, y, width, height)

def spawn_random_enemy(exclude=None):
    if exclude is None:
        exclude = []
    enemy_classes = [BlueEnemy, RedEnemy, YellowEnemy, GreenEnemy, PurpleEnemy]
    allowed = [enemy for enemy in enemy_classes if enemy not in exclude]
    chosen_class = random.choice(allowed)
    return chosen_class


@property
def finished(self):
    return self.current_wave >= len(self.waves) and not self.enemies
