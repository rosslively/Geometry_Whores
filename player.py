import pygame
import math
from assets import Assets
assets = Assets.load_assets()
from ui import Ui
kill_sound = assets["kill_sound"]
death_sound = assets["death_sound"]
debug_mode = False
class Player:

    def __init__(self, image, start_pos=(375, 500), speed=6):
        self.image_orig = image
        self.image_size = (120, 120)
        self.image_orig = pygame.transform.scale(self.image_orig, self.image_size)
        self.image = self.image_orig
        self.rect = self.image.get_rect(center=start_pos)
        self.angle = 0
        self.speed = speed
        self.original_image = image
        self.invulnerable_until = 0
        self.blink_toggle = True
        self.last_blink_time = 0
        self.death_shockwave_time = 0
        self.bomb_shockwave_time = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.death_shockwave_active = False
        

    def rescale(self):
        self.image = pygame.transform.scale(self.image_orig, self.image_size)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)   

    def move(self, keys, boundary_rect):
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.Rect(boundary_rect))

    def rotate(self, mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))
        self.angle -= 90 

        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self, screen):
        now = pygame.time.get_ticks()
        # -1 life shockwave
        if now < self.death_shockwave_time + 500:
            elapsed = now - self.death_shockwave_time
            radius = 30 + (elapsed / 500) * 400  # Expands to 400px over 0.5s
            alpha = max(0, 255 - int((elapsed / 500) * 255))
            shockwave_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shockwave_surface, (255, 0, 0, alpha), (radius, radius), radius, width=5)
            screen.blit(shockwave_surface, (self.rect.centerx - radius, self.rect.centery - radius))

        
        # Bomb Shockwave drawing
        if now < self.bomb_shockwave_time + 500:
            elapsed = now - self.bomb_shockwave_time
            radius = 30 + (elapsed / 1200) * 800
            alpha = max(0, 255 - int((elapsed / 500) * 255))
            shockwave_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shockwave_surface, (255, 255, 255, alpha), (radius, radius), int(radius), width=5)
            screen.blit(shockwave_surface, (self.rect.centerx - radius, self.rect.centery - radius))

        
        
        draw_player = True
        if now < self.invulnerable_until:
            if now - self.last_blink_time > 100:
                self.blink_toggle = not self.blink_toggle
                self.last_blink_time = now
            draw_player = self.blink_toggle

        if draw_player:
            screen.blit(self.image, self.rect)

        if debug_mode:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
            if self.mask:
                mask_surface = self.mask.to_surface(setcolor=(255, 0, 0, 100), unsetcolor=(0, 0, 0, 0))
                screen.blit(mask_surface, self.rect.topleft)

    def get_position(self):
        return self.rect.center

    def get_rect(self):
        return self.rect

    def get_angle(self):
        return self.angle
    
    def rescale(self):
        width, height = Ui.get_dimensions()
        scale_factor = height / 600
        new_size = (int(self.original_image.get_width() * scale_factor),
                    int(self.original_image.get_height() * scale_factor))
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect(center=self.rect.center if hasattr(self, "rect") else (width // 2, height // 2))

    def bomb_shockwave(self, enemies, bomb_sound, score):
        now = pygame.time.get_ticks()
        if now < self.bomb_shockwave_time + 500:
            elapsed = now - self.bomb_shockwave_time
            radius = 30 + (elapsed / 800) * 800
            shockwave_center = self.rect.center
            bomb_sound.play()
            for enemy in enemies[:]:
                dx = enemy.rect.centerx - shockwave_center[0]
                dy = enemy.rect.centery - shockwave_center[1]
                distance = math.hypot(dx, dy)

                if distance < radius:
                    kill_sound.play()
                    enemies.remove(enemy)
                    score += 100
        return score
    
    def death_shockwave(self, enemies, lives):
        now = pygame.time.get_ticks()

        if now < self.death_shockwave_time + 500:
            elapsed = now - self.death_shockwave_time
            radius = 40 + (elapsed / 600) * 800
            shockwave_center = self.rect.center
            

            for enemy in enemies[:]:
                dx = enemy.rect.centerx - shockwave_center[0]
                dy = enemy.rect.centery - shockwave_center[1]
                distance = math.hypot(dx, dy)

                if distance < radius:
                    kill_sound.play()
                    enemies.remove(enemy)
            return enemies, lives
        else:
            self.death_shockwave_active = False
            return enemies, lives
