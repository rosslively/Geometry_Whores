import pygame
from font import Font
from config import WIDTH, HEIGHT
from run_game import high_score
from ui import Ui
Font.rescale_fonts(height=HEIGHT)
font_large = Font.get_large()
font_small = Font.get_small()
class Game_over:
    @staticmethod
    def show_game_over_screen(score, high_score, render_surface):
        font_large = Font.get_large()
        font_small = Font.get_small()
        screen = Ui.get_screen()
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q:
                        return False

            render_surface.fill((0, 0, 0))

            if score >= high_score:
                line1 = font_large.render("High Score!", True, (255, 255, 0))
                line2 = font_small.render(f"{high_score}", True, (255, 255, 0))
                prompt = font_small.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
                
                render_surface.blit(line1, (WIDTH // 2 - line1.get_width() // 2, HEIGHT // 2 - 50))
                render_surface.blit(line2, (WIDTH // 2 - line2.get_width() // 2, HEIGHT // 2 - 10))
                render_surface.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))
            else:
                line3 = font_large.render("Game Over", True, (255, 0, 0))
                prompt = font_small.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
                
                render_surface.blit(line3, (WIDTH // 2 - line3.get_width() // 2, HEIGHT // 2 - 50))
                render_surface.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))

            window_width, window_height = Ui.get_dimensions()
            render_width, render_height = render_surface.get_size()

            scale_x = window_width / render_width
            scale_y = window_height / render_height
            scale = min(scale_x, scale_y)

            scaled_width = int(render_width * scale)
            scaled_height = int(render_height * scale)

            x = (window_width - scaled_width) // 2
            y = (window_height - scaled_height) // 2

            scaled_frame = pygame.transform.smoothscale(render_surface, (scaled_width, scaled_height))

            screen.fill((0, 0, 0))
            screen.blit(scaled_frame, (x, y))

            pygame.display.flip()
            clock.tick(60)
