import pygame
from config import WIDTH, HEIGHT, FPS
from assets import Assets
from player import Player
from bullet import Bullet
from spawn_manager import SpawnManager
from ui import Ui
from pause import Pause
from score import load_high_score, save_high_score

pygame.init()
assets = Assets.load_assets()
screen = Ui.initialize(WIDTH, HEIGHT, "Geometry Whores", assets["icon"])
Ui.width, Ui.height = WIDTH, HEIGHT
render_surface = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
waves = 1
running = True
score = 0
bombs = 0
lives = 0
next_bomb_score = 10000
next_life_score = 20000
high_score = load_high_score()
high_score = 0


def handle_enemy_collisions(enemies, bullets, score, kill_sound):
    for enemy in enemies[:]: 
        for bullet in bullets[:]:
            if enemy.rect.colliderect(bullet.rect):
                offset = (bullet.rect.left - enemy.rect.left, bullet.rect.top - enemy.rect.top)
                if enemy.mask.overlap(bullet.mask, offset):
                    kill_sound.play()
                    enemy.health -= 1
                    score += 100
                    bullets.remove(bullet)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                    break
    return score

class Run:
    @staticmethod
    def run_game(screen, current_score=0, high_score=None):
        if high_score is None:
            high_score = load_high_score()
            global waves, bombs, lives
            score = current_score
            game_over_sound = assets["game_over_sound"]
            bullet_sound = assets["bullet_sound"]
            kill_sound = assets["kill_sound"]
            bomb_sound = assets["bomb_sound"]
            death_sound = assets["death_sound"]
            player = Player(assets["player_image"])
            bullets = []
            active_enemies = []
            bombs = 3
            next_bomb_score = 10000
            lives = 2
            
            next_life_score = 20000
            spawn_area = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
            spawn_manager = SpawnManager(active_enemies, spawn_area)

            bullet_cooldown = 200
            last_shot_time = 0
            boundary_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

            last_window_size = Ui.get_dimensions()
            render_width, render_height = render_surface.get_size()
            scale_x = last_window_size[0] / render_width
            scale_y = last_window_size[1] / render_height
            scale = min(scale_x, scale_y)
            scaled_width = int(render_width * scale)
            scaled_height = int(render_height * scale)
            x = (last_window_size[0] - scaled_width) // 2
            y = (last_window_size[1] - scaled_height) // 2

            while True:
                dt = clock.tick(FPS)
                current_time = pygame.time.get_ticks()
                resize_pending = False
                new_size = last_window_size
                hearts = lives + 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False, score, high_score
                    
                    elif event.type == pygame.VIDEORESIZE:
                        new_size = (event.w, event.h)
                        resize_pending = True, score, high_score

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pause_action = Pause.pause_menu(render_surface, score, high_score, player, bullets, active_enemies, hearts, bombs, offset_x, offset_y)
                            if pause_action == "resume":
                                clock.tick()
                                continue
                            elif pause_action == "quit":
                                return False, score, high_score
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e and bombs > 0:
                            bombs -= 1
                            player.bomb_shockwave_time = pygame.time.get_ticks()
                            
                if resize_pending and new_size != last_window_size:
                    screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)
                    Ui.update_window_size(*new_size)
                    last_window_size = new_size
                    player.rescale()
                    for enemy in active_enemies:
                        enemy.rescale()

                    render_width, render_height = render_surface.get_size()
                    scale_x = new_size[0] / render_width
                    scale_y = new_size[1] / render_height
                    scale = min(scale_x, scale_y)
                    scaled_width = int(render_width * scale)
                    scaled_height = int(render_height * scale)
                    x = (new_size[0] - scaled_width) // 2
                    y = (new_size[1] - scaled_height) // 2

                    

                parallax_factor = 0.04

                player_pos = player.get_position()
                offset_x = player_pos[0] * parallax_factor
                offset_y = player_pos[1] * parallax_factor

                Ui.draw_background(render_surface, (offset_x, offset_y))
                Ui.draw_score(render_surface, score, high_score)
                Ui.draw_status(render_surface, score, high_score, hearts, bombs)

                keys = pygame.key.get_pressed()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                scaled_mouse = (mouse_x * WIDTH / last_window_size[0], mouse_y * HEIGHT / last_window_size[1])

                player.move(keys, boundary_rect)
                player.rotate(scaled_mouse)
                player.draw(render_surface)

                spawn_manager.update(WIDTH, HEIGHT)
                if spawn_manager.finished:
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    return True, score, high_score
                
                for enemy in active_enemies[:]:
                    enemy.update(player.get_position(), dt)
                    if not enemy.is_harmless and player.rect.colliderect(enemy.rect):
                        offset = (enemy.rect.left - player.rect.left, enemy.rect.top - player.rect.top)
                        if player.mask.overlap(enemy.mask, offset):
                            current_time = pygame.time.get_ticks()
                            if current_time > player.invulnerable_until:
                                lives -= 1
                                hearts -=1
                                player.invulnerable_until = current_time + 2000
                                player.death_shockwave_time = current_time
                                player.death_shockwave_active = True
                                death_sound.play()
                                if lives < 0:
                                    game_over_sound.play()
                                    if score > high_score:
                                        high_score = score
                                        save_high_score(high_score)
                                    return True, score, high_score

                if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and current_time - last_shot_time > bullet_cooldown:
                    bullets.append(Bullet(player.get_position(), player.get_angle()))
                    bullet_sound.play()
                    last_shot_time = current_time

                for bullet in bullets[:]:
                    bullet.update()
                    bullet.draw(render_surface)
                    if bullet.off_screen(WIDTH, HEIGHT):
                        bullets.remove(bullet)
                        
                score = handle_enemy_collisions(active_enemies, bullets, score, kill_sound)
                if score >= next_bomb_score:
                    bombs += 1
                    next_bomb_score += 10000
                
                if score >= next_life_score:
                    lives += 1
                    next_life_score += 20000
                
                for enemy in active_enemies:
                    enemy.draw(render_surface)

                score = player.bomb_shockwave(active_enemies, bomb_sound, score)
                if player.death_shockwave_active:
                    active_enemies, lives = player.death_shockwave(active_enemies, lives)
                scaled_frame = pygame.transform.smoothscale(render_surface, (scaled_width, scaled_height))
                
                screen = Ui.get_screen()
                screen.fill((0, 0, 0))
                screen.blit(scaled_frame, (x, y))
                
                pygame.display.flip()
