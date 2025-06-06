import pygame
from font import Font
from ui import Ui

class Pause:
    def pause_menu(render_surface, score, high_score, player, bullets, enemies, hearts, bombs, offset_x, offset_y):
        font_large = Font.get_large()
        font_small = Font.get_small()
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "resume"
                    elif event.key == pygame.K_q:
                        return "quit"

            render_surface.fill((0, 0, 0))

            Ui.draw_background(render_surface, (offset_x, offset_y))

            Ui.draw_score(render_surface, score, high_score)

            Ui.draw_status(render_surface, score, high_score, hearts, bombs)

            for enemy in enemies:
                enemy.draw(render_surface)

            for bullet in bullets:
                bullet.draw(render_surface)

            player.draw(render_surface)

            paused_text = font_large.render("Paused", True, (255, 255, 255))
            render_surface.blit(
                paused_text,
                (render_surface.get_width() // 2 - paused_text.get_width() // 2,
                render_surface.get_height() // 2 - 60)
            )

            prompt = font_small.render("Press ESC to Resume or Q to Quit", True, (255, 255, 255))
            render_surface.blit(
                prompt,
                (render_surface.get_width() // 2 - prompt.get_width() // 2,
                render_surface.get_height() // 2 + 10)
            )

            window_width, window_height = Ui.get_dimensions()
            scale_x = window_width / render_surface.get_width()
            scale_y = window_height / render_surface.get_height()
            scale = min(scale_x, scale_y)

            scaled_frame = pygame.transform.smoothscale(
                render_surface,
                (int(render_surface.get_width() * scale), int(render_surface.get_height() * scale))
            )

            x = (window_width - scaled_frame.get_width()) // 2
            y = (window_height - scaled_frame.get_height()) // 2

            screen = Ui.get_screen()
            screen.fill((0, 0, 0))
            screen.blit(scaled_frame, (x, y))
            pygame.display.flip()
