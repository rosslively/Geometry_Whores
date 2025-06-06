import pygame
from utils import resource_path
screen = pygame.display.set_mode((800, 600))
pygame.mixer.init()

class Assets:
    @staticmethod
    def load_assets():

        # Images
        background_image = pygame.image.load(resource_path('assets/stars.png')).convert_alpha()
        player_image = pygame.image.load(resource_path('assets/player.png')).convert_alpha()
        blue_enemy = pygame.image.load(resource_path('assets/blue_enemy.png')).convert_alpha()
        green_enemy = pygame.image.load(resource_path('assets/green_enemy.png')).convert_alpha()
        purple_enemy = pygame.image.load(resource_path('assets/purple_enemy.png')).convert_alpha()
        red_enemy = pygame.image.load(resource_path('assets/red_enemy.png')).convert_alpha()
        yellow_enemy = pygame.image.load(resource_path('assets/yellow_enemy.png')).convert_alpha()
        tank_enemy = pygame.image.load(resource_path('assets/tank_enemy.png')).convert_alpha()
        bullet_image = pygame.image.load(resource_path('assets/bullet.png')).convert_alpha()   
        icon = pygame.image.load(resource_path("assets/icon.png"))
        bomb_image = pygame.image.load(resource_path("assets/bomb.png"))
        heart_image = pygame.image.load(resource_path("assets/heart.png"))
        # Sounds
        bullet_sound = pygame.mixer.Sound(resource_path("sounds/bullet_sound.wav"))
        kill_sound = pygame.mixer.Sound(resource_path("sounds/kill_sound.wav"))
        game_over_sound = pygame.mixer.Sound(resource_path("sounds/game_over_sound.mp3"))
        bomb_sound = pygame.mixer.Sound(resource_path("sounds/bomb_sound.wav"))
        spawn_sound = pygame.mixer.Sound(resource_path("sounds/spawn_sound.wav"))
        death_sound = pygame.mixer.Sound(resource_path("sounds/death_sound.wav"))


        try:
            with open(resource_path("assets/highscore.txt"), "r") as f:
                high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            high_score = 0 

        return {
            "background_image": background_image,
            "player_image": player_image,
            "blue_enemy": blue_enemy,
            "green_enemy": green_enemy,
            "purple_enemy": purple_enemy,
            "red_enemy": red_enemy,
            "yellow_enemy": yellow_enemy,
            "tank_enemy": tank_enemy,
            "bullet_image": bullet_image,
            "icon": icon,
            "high_score": high_score,
            "heart_image": heart_image,
            "bomb_image": bomb_image,

            "bullet_sound": bullet_sound,
            "kill_sound": kill_sound,
            "game_over_sound": game_over_sound,
            "bomb_sound": bomb_sound,
            "spawn_sound": spawn_sound,
            "death_sound": death_sound
        }