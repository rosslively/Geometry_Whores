import pygame
from assets import Assets
from font import Font
from config import WIDTH, HEIGHT
assets = Assets.load_assets()
from utils import resource_path
assets["heart_icon"] = pygame.image.load(resource_path("assets/heart.png")).convert_alpha()
assets["bomb_icon"] = pygame.image.load(resource_path("assets/bomb.png")).convert_alpha()
assets["heart_icon"] = pygame.transform.scale(assets["heart_icon"], (24, 24))
assets["bomb_icon"] = pygame.transform.scale(assets["bomb_icon"], (24, 24))

class Ui:
    screen = None
    scaled_background = None
    icon = None
    assets = None
    width = WIDTH
    height = HEIGHT

    @staticmethod
    def initialize(width=WIDTH, height=HEIGHT, title="Geometry Whores", icon=None):
        Ui.assets = Assets.load_assets()
        if icon is None:
            Ui.icon = Ui.assets["icon"]
        else:
            Ui.icon = icon
        Ui.scaled_background = Ui.assets["background_image"]
        Ui.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        pygame.display.set_icon(Ui.icon)
        Ui.width, Ui.height = width, height
        Ui.rescale_ui()
        return Ui.screen

    @staticmethod
    def update_window_size(new_width, new_height):
        Ui.width, Ui.height = new_width, new_height
        Ui.screen = pygame.display.set_mode((Ui.width, Ui.height), pygame.RESIZABLE)
        Ui.rescale_ui()

    @staticmethod
    def rescale_ui(width=None, height=None):
        if width is None:
            width = Ui.width
        if height is None:
            height = Ui.height

        Ui.scaled_background = pygame.transform.scale(
            Ui.assets["background_image"],
            (int(WIDTH * 1.2), int(HEIGHT * 1.2))
        )
        Font.rescale_fonts(height)

    @staticmethod
    def draw_background(surface, offset=(0, 0)):
        bg = Ui.scaled_background

        draw_x = int(-offset[0])
        draw_y = int(-offset[1])

        surface.blit(bg, (draw_x, draw_y))


    @staticmethod
    def draw_score(surface, score, high_score):
        font_small = Font.get_small()
        font_color = (255, 255, 255)
        width, height = surface.get_size()
        score_text = font_small.render(f"Score: {score}", True, font_color)
        surface.blit(score_text, (width - score_text.get_width() - 10, 10))

        high_score_text = font_small.render(
            f"High Score: {max(score, high_score)}", True, font_color
        )
        surface.blit(high_score_text, (width - high_score_text.get_width() - 10, 40))

    @staticmethod
    def draw_status(surface, score, high_score, hearts, bombs):
        x, y = 20, 20
        spacing = 30  # Space between icons

        # Draw hearts for lives
        for i in range(hearts):
            surface.blit(assets["heart_icon"], (x + i * spacing, y))

        # Draw bombs after hearts
        bomb_start_x = x + (hearts * spacing) + 20  # Add gap after hearts
        for i in range(bombs):
            surface.blit(assets["bomb_icon"], (bomb_start_x + i * spacing, y))


    @staticmethod
    def get_screen():
        return pygame.display.get_surface()

    @staticmethod
    def get_dimensions():
        dims = Ui.screen.get_size()
        return dims


