import pygame
import math

debug_mode = False

class Bullet:
    def __init__(self, pos, angle, speed=15):
        self.surface = pygame.Surface((8, 8), pygame.SRCALPHA) 
        pygame.draw.circle(self.surface, (214, 200, 36), (4, 4), 4)
        self.rect = self.surface.get_rect(center=pos)
        rad_angle = math.radians(angle + 90)
        self.dir = (math.cos(rad_angle), math.sin(rad_angle))
        self.speed = speed
        self.color = (127, 127, 127)

        self.mask = pygame.mask.from_surface(self.surface)

        
    def update(self):
        self.rect.x += self.dir[0] * self.speed
        self.rect.y += self.dir[1] * self.speed

    def draw(self, screen):
        if not getattr(self, 'visible', True):
            return
        if hasattr(self, 'surface') and self.surface:
            screen.blit(self.surface, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        if debug_mode:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)

            if hasattr(self, 'mask') and self.mask:
                mask_surface = self.mask.to_surface(setcolor=(255, 0, 0, 100), unsetcolor=(0, 0, 0, 0))
                screen.blit(mask_surface, self.rect.topleft)

    def off_screen(self, width, height):
        return (self.rect.right < 0 or self.rect.left > width or
                self.rect.bottom < 0 or self.rect.top > height)
