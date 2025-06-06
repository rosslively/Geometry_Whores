import pygame
import sys
from run_game import render_surface, Run
from score import load_high_score, reset_score
from game_over import Game_over
from font import Font

def main():
    pygame.init()
    Font.rescale_fonts(render_surface.get_height())
    high_score = load_high_score()
    score = 0
    while True:
        result, score, high_score = Run.run_game(render_surface, score,)
        if not result:
            break
        restart = Game_over.show_game_over_screen(score, high_score, render_surface)
        if not restart:
            
            break
        score = reset_score()    

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
