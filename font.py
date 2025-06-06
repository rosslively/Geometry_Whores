import pygame
from config import HEIGHT
pygame.init()

class Font:
    font_small = None
    font_large = None

    @staticmethod
    def rescale_fonts(height):
        Font.font_small = pygame.font.Font(None, max(12, int(height * 0.03)))
        Font.font_large = pygame.font.Font(None, max(24, int(height * 0.06)))

    @staticmethod
    def get_small():
        return Font.font_small

    @staticmethod
    def get_large():
        return Font.font_large

Font.rescale_fonts(HEIGHT)
    
font_small = Font.get_small()
font_large = Font.get_large()
