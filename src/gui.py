
import logging
import pygame
import pygame_menu
import pygame_menu.themes
from pyjack import Player, Game

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.SysFont('Arial', 24)

# Constans
MENU_DIFFICULTY=[('Easy', 1)]

# Settings
NR_PLAYERS = 1
DIFFICULTY = ('Easy', 1)

def draw_text(surface, text, x, y, color=BLACK):
    text_surface = FONT.render(text, True, color)
    surface.blit(text_surface, (x, y))

def get_main_menu():
    main_menu = pygame_menu.Menu('Welcome', 600, 400, theme=pygame_menu.themes.THEME_DARK)
    main_menu.add.text_input('Players: ', default=NR_PLAYERS)
    main_menu.add.dropselect('Difficulty: ', items=MENU_DIFFICULTY, onchange=set_difficulty)
    main_menu.add.button('Start', start_game)
    main_menu.add.button('Quit', exit)
    return main_menu

def start_game():
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        game = Game(host_name='Croupier', players=[Player('p%s' % i) for i in range(1, NR_PLAYERS)])
        game.main_loop(1)

        pygame.display.update()
        clock.tick(30)


def set_difficulty(value, difficulty):
    DIFFICULTY = value

def main():
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Card Game')

    main_menu = get_main_menu()

    main_menu.mainloop(surface)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(lineno)d:%(funcName)s - %(message)s")
    main()

