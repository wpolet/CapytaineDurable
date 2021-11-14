import pygame as pg

import globvars as glob
from menu import Menu
from game import Game
from settings import WIDTH, HEIGHT
from persistence import Persistence

# Get initial parameters
glob.persistence = Persistence()
glob.persistence.get_saved_games()

# Pygame initialization:
pg.init()
pg.display.set_caption("Capytaine Durable")
glob.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN if glob.user_config['fullscreen_mode'] else 0)

menu = Menu()

while glob.active_screen == "mainmenu":
    menu.show_main_menu()
    menu.main_menu_events()

    # Game management
    if glob.active_screen == "capytaine":
        game = Game(menu.game_params)
        while glob.active_screen == "capytaine":
            game.update()
            game.display()
            game.game_events()
