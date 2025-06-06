import pygame
import math
from assets import Assets

assets = Assets.load_assets()
blue_enemy = assets["blue_enemy"]
green_enemy = assets["green_enemy"]
purple_enemy = assets["purple_enemy"]
red_enemy = assets["red_enemy"]
yellow_enemy = assets["yellow_enemy"]
tank_enemy = assets["tank_enemy"]

debug_mode = False
class Enemy:
    def __init__(self, pos, size=1, speed=1, color=(255, 255, 0), image = None, image_size = None, health=1, shrink_rect_by=(0, 0)):
        x, y = pos
        self.speed = speed
        self.color = color
        self.image = image
        self.harmless_timer = 2000
        self.spawn_time = pygame.time.get_ticks()
        self.is_harmless = True
        self.blink_interval = 200
        self.last_blink_time = self.spawn_time
        self.visible = True
        self.health = health

        if image:
            self.original_image = image
            self.image_size = image_size or (image.get_width(), image.get_height())
            self.image = pygame.transform.scale(self.original_image, self.image_size)
            self.rect = self.image.get_rect(center=pos)

            if shrink_rect_by != (0, 0):
                center = self.rect.center
                self.rect = self.rect.inflate(-shrink_rect_by[0], -shrink_rect_by[1])
                self.rect.center = center

            self.pos_x = float(self.rect.centerx)
            self.pos_y = float(self.rect.centery)
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.rect = pygame.Rect(x, y, size, size)
            if shrink_rect_by != (0, 0):
                center = self.rect.center
                self.rect = self.rect.inflate(-shrink_rect_by[0], -shrink_rect_by[1])
                self.rect.center = center

    def rescale(self):
        self.image = pygame.transform.scale(self.original_image, self.image_size)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def update(self, target_pos, dt):
        now = pygame.time.get_ticks()
        
        if self.harmless_timer > 0:
            self.harmless_timer -= dt
            if self.harmless_timer <= 0:
                self.is_harmless = False
                self.visible = True  
            else:
                
                if not hasattr(self, 'last_blink_time'):
                    self.last_blink_time = now
                    self.visible = True

                blink_interval = 200
                if now - self.last_blink_time > blink_interval:
                    self.visible = not self.visible
                    self.last_blink_time = now
        else:
            self.visible = True

        if not self.is_harmless:
            dx = target_pos[0] - self.pos_x
            dy = target_pos[1] - self.pos_y
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx /= distance
                dy /= distance
                self.pos_x += dx * self.speed * dt / 16
                self.pos_y += dy * self.speed * dt / 16
                self.rect.centerx = int(self.pos_x)
                self.rect.centery = int(self.pos_y)

    def draw(self, screen):
        if not getattr(self, 'visible', True):
            return
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        if debug_mode:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)

            if hasattr(self, 'mask') and self.mask:
                mask_surface = self.mask.to_surface(setcolor=(255, 0, 0, 100), unsetcolor=(0, 0, 0, 0))
                screen.blit(mask_surface, self.rect.topleft)
    
class BlueEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, size=5, speed=3, image=blue_enemy, image_size=(20, 20), health=1)

class RedEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, size=4, speed=2, image=red_enemy, image_size=(20, 20), health=1)

class YellowEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, size=4, speed=4, image=yellow_enemy, image_size=(20, 20), health=1)

class GreenEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, size=6, speed=5, image=green_enemy, image_size=(20, 20), health=1)

class PurpleEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, size=1, speed=6, image=purple_enemy, image_size=(60, 60), health=1,)

class TankEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, size=5, speed=1, image=tank_enemy, image_size=(150, 150), health=50)

