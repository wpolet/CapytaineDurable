"""
    This module manages the start menu of the game.

    Class
    -----
    Menu:
        a class used to manage start of the game with main menu and
        the player selection or loading a saved game
"""

import pygame as pg
from datetime import datetime

import globvars as glob
from capylib import draw_text, get_hovered_rectangle, exit_gracefully
from settings import *


class Menu:
    """
        A class used to manage start of the game with main menu and
        the player selection or loading a saved game.

        Attributes
        ----------
        hovered_item: dictionary ID of Rect object
            Holds id of rectangle currently hovered by mouse pointer
        hovered_item_previous: dictionary ID of Rect object
            Holds id of last hovered rectangle to allow detection of state changes
        game_params: dictionary
            saved game parameters or default parameters from 'settings.py'
        clickable_item: dictionary of Rect object
            contains all rectangles that must react to mouse events
        players_image: list of Surface object
            list of character images that the user can select

        Methods
        -------
        show_main_menu(self):
            screen displayed at game lauch
        main_menu_events(self):
            manages user actions in the menu
        main_menu_validation_handler(self):
            processes the exit from the main menu
        show_player_selection_screen(self):
            screen displayed at new game lauch to select the character to play with
        player_selection_events(self):
            manages user actions in the player selection screen
        show_load_screen(self):
            screen displayed to select a previously saved game
        load_screen_events(self):
            manages user actions in the load menu
        load_validation_handler(self):
            processes the exit from the load menu
    """

    def __init__(self):
        self.whoami = __name__

        # Pygame setup:
        pg.key.set_repeat()

        # Game default parameters
        self.game_params = GAME_STARTUP_PARAMS

        # Variables:
        self.hovered_item = None
        self.hovered_item_previous = None
        self.clickable_item = {}

        self.mainmenu_bkg = pg.image.load(IMAGEDIR + 'bkg-old-paper.jpg')
        self.loadmenu_bkg = pg.image.load(IMAGEDIR + 'bkg-swirls.jpg')
        self.select_right = pg.image.load(IMAGEDIR + 'select_right.png')
        self.select_left = pg.image.load(IMAGEDIR + 'select_left.png')
        self.selection_rect = pg.Surface((58, 64))
        self.selection_rect.fill(GREEN)
        self.players_image = []
        for i in range(0, 8):
            self.players_image.append(
                pg.transform.scale2x(pg.image.load(IMAGEDIR + 'player/player' + str(i) + '_s.png').convert_alpha()))

    def show_main_menu(self):
        """ Screen displayed at game lauch.

        Variable user_selection is an integer that the user can increment or decrement
        by pressing the up arrow and the down arrow respectively (see 'main_menu_events' function).

        Menu items are stored in 'settings.py'

        :return: None
        """

        self.clickable_item = {}
        glob.screen.fill(BLACK)
        glob.screen.blit(self.mainmenu_bkg, (0, 0))

        # Draw title:
        draw_text(self, "Capytaine Durable", 50, (WIDTH/2, 170), "midtop", BLACK)

        for idx in range(len(MAINMENU_ITEMS)):
            text = MAINMENU_ITEMS[idx][1]

            # Special case management:
            if MAINMENU_ITEMS[idx][0] == "displaymode":
                text += " : " + ("Plein écran" if glob.user_config["fullscreen_mode"] else "Fenêtré")

            if glob.user_selection != idx:
                fontsize = 25
            else:
                fontsize = 30

                # Draw selection arrows:
                font = pg.font.Font(pg.font.match_font(DEFAULTFONT), fontsize)
                text_surface = font.render(' ' + text + ' ', True, BLACK)
                text_width = text_surface.get_width()
                position_left = (WIDTH/2 - text_width/2 - TILESIZE, HEIGHT/2 - 47 + idx*50)
                position_right = (WIDTH/2 + text_width/2, HEIGHT/2 - 47 + idx*50)

                glob.screen.blit(self.select_left, position_left)
                glob.screen.blit(self.select_right, position_right)

            position = (WIDTH/2, HEIGHT/2 - 50 + idx*50)
            draw_text(self, text, fontsize, position, "midtop", BLACK, MAINMENU_ITEMS[idx][0])

        draw_text(self, "Version " + str(VERSION), 20, (WIDTH, HEIGHT), "bottomright")

        pg.display.flip()

        if DEBUG:
            print("Main menu page refreshed at", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def main_menu_events(self):
        """ Manages user actions in the menu.

        Actions catched as pygame events
        Type:   - MOUSEMOTION
                - MOUSEBUTTONUP
                - KEYDOWN

        :return: None
        """

        user_is_inactive = True
        while user_is_inactive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_gracefully(self)

                elif event.type == pg.MOUSEMOTION:
                    self.hovered_item = get_hovered_rectangle(self.clickable_item, event.pos)
                    if self.hovered_item is not None:
                        for idx in range(len(MAINMENU_ITEMS)):
                            if MAINMENU_ITEMS[idx][0] == self.hovered_item and self.hovered_item_previous != self.hovered_item:
                                glob.user_selection = idx
                                user_is_inactive = False
                                self.hovered_item_previous = self.hovered_item
                                break

                elif event.type == pg.MOUSEBUTTONUP:
                    if get_hovered_rectangle(self.clickable_item, event.pos) is not None:
                        user_is_inactive = False
                        self.main_menu_validation_handler()

                elif event.type == pg.KEYDOWN:
                    user_is_inactive = False
                    if event.key == pg.K_DOWN:
                        glob.user_selection += 1
                        if glob.user_selection >= len(MAINMENU_ITEMS):
                            glob.user_selection = 0
                    elif event.key == pg.K_UP:
                        glob.user_selection -= 1
                        if glob.user_selection < 0:
                            glob.user_selection = len(MAINMENU_ITEMS) - 1
                    elif event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        self.main_menu_validation_handler()

            if user_is_inactive:
                pg.time.wait(SLEEPTIME)

    def main_menu_validation_handler(self):
        """ Processes the exit from the main menu.

        :return: None
        """

        if MAINMENU_ITEMS[glob.user_selection][0] == "startgame":
            self.game_params = GAME_STARTUP_PARAMS  # Reset parameters
            glob.active_screen = "playerselection"
            while glob.active_screen == "playerselection":
                self.show_player_selection_screen()
                self.player_selection_events()
            glob.user_selection = 0
        elif MAINMENU_ITEMS[glob.user_selection][0] == "loadgame":
            glob.active_screen = "loadscreen"
            while glob.active_screen == "loadscreen":
                self.show_load_screen()
                self.load_screen_events()
            glob.user_selection = 0
        elif MAINMENU_ITEMS[glob.user_selection][0] == "displaymode":
            glob.user_config['fullscreen_mode'] = not glob.user_config['fullscreen_mode']
            glob.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN if glob.user_config['fullscreen_mode'] else 0)
        elif MAINMENU_ITEMS[glob.user_selection][0] == "quitmenu":
            exit_gracefully(self)

    def show_player_selection_screen(self):
        """ Screen displayed at new game lauch to select the character to play with.

        :return: None
        """

        self.clickable_item = {}
        glob.screen.fill(BLACK)
        glob.screen.blit(self.mainmenu_bkg, (0, 0))

        draw_text(self, "Choisis un avatar", 25, (WIDTH / 2, 100), "midtop", DARKGREY)

        x = (2 * WIDTH) / 5
        y = HEIGHT / 2 - 150


        for p in range(0, 8):
            if p == 4:
                x = (3 * WIDTH) / 5
                y = HEIGHT / 2 - 150

            if glob.user_selection == p:
                if p < 4:
                    glob.screen.blit(self.selection_rect, (x - 8, y - 4))
                else:
                    glob.screen.blit(self.selection_rect, (x, y - 4))

            glob.screen.blit(self.players_image[p], (x, y))
            self.clickable_item['AVATAR' + str(p)] = self.players_image[p].get_rect(topleft=(x, y))

            y += 75

        pg.display.flip()

        if DEBUG:
            print("Player selection screen refreshed at", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def player_selection_events(self):
        """ Manages user actions in the player selection screen.

        Actions catched as pygame events
        Type:   - MOUSEMOTION
                - MOUSEBUTTONUP
                - KEYDOWN

        :return: None
        """

        user_is_inactive = True
        while user_is_inactive:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    exit_gracefully(self)

                elif event.type == pg.MOUSEMOTION:
                    self.hovered_item = get_hovered_rectangle(self.clickable_item, event.pos)
                    if self.hovered_item is not None:
                        for idx in range(8):
                            if 'AVATAR' + str(
                                    idx) == self.hovered_item and self.hovered_item_previous != self.hovered_item:
                                glob.user_selection = idx
                                user_is_inactive = False
                                self.hovered_item_previous = self.hovered_item
                                break

                elif event.type == pg.MOUSEBUTTONUP:
                    if get_hovered_rectangle(self.clickable_item, event.pos) is not None:
                        user_is_inactive = False
                        self.game_params['player']['name'] = 'player' + str(glob.user_selection)
                        glob.active_screen = "capytaine"

                elif event.type == pg.KEYDOWN:
                    user_is_inactive = False
                    if event.key == pg.K_ESCAPE:
                        glob.active_screen = "mainmenu"
                        glob.user_selection = 0
                    elif event.key == pg.K_DOWN and (glob.user_selection % 4) < 3:
                        glob.user_selection += 1
                    elif event.key == pg.K_UP and (glob.user_selection % 4) > 0:
                        glob.user_selection -= 1
                    elif event.key == pg.K_RIGHT and glob.user_selection < 4:
                        glob.user_selection += 4
                    elif event.key == pg.K_LEFT and glob.user_selection > 3:
                        glob.user_selection -= 4
                    elif event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        self.game_params['player']['name'] = 'player' + str(glob.user_selection)
                        glob.active_screen = "capytaine"

            if user_is_inactive:
                pg.time.wait(SLEEPTIME)

    def show_load_screen(self):
        """ Screen displayed to select a previously saved game.

        :return: None
        """

        self.clickable_item = {}
        glob.screen.fill(BLACK)
        glob.screen.blit(self.loadmenu_bkg, (0, 0))

        draw_text(self, "Charger une partie", 25, (WIDTH / 2, 60), "midtop", DARKGREY)

        for idx in range(SAVESLOTS):
            if glob.saved_games[idx]['timestamp'] > datetime.min:
                if glob.user_selection != idx:
                    fontsize = 20
                    color = BROWN
                else:
                    fontsize = 25
                    color = GREEN
                draw_text(self, glob.saved_games[idx]['timestamp'].strftime("%m/%d/%Y, %H:%M:%S"), fontsize,
                          (WIDTH / 2, HEIGHT / 2 - 200 + (idx * 50)), "midtop", color, 'SLOT' + str(idx))
            else:
                draw_text(self, "VIDE", 20, (WIDTH / 2, HEIGHT / 2 - 200 + (idx * 50)), "midtop",
                          BROWN if glob.user_selection != idx else DARKGREY, 'SLOT' + str(idx))

        draw_text(self, "RETOUR", 20, (WIDTH / 2, HEIGHT / 2 - 200 + (SAVESLOTS * 50)), "midtop",
                  DARKGREY if glob.user_selection < SAVESLOTS else GREEN, 'BACK')

        pg.display.flip()
        if DEBUG:
            print("Load page refreshed at", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def load_screen_events(self):
        """ Manages user actions in the menu.

        Actions catche as pygame events
        Type:   - MOUSEMOTION
                - MOUSEBUTTONUP
                - KEYDOWN

        :return: None
        """

        user_is_inactive = True
        while user_is_inactive:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    exit_gracefully(self)

                elif event.type == pg.MOUSEMOTION:
                    self.hovered_item = get_hovered_rectangle(self.clickable_item, event.pos)
                    if self.hovered_item is not None:
                        for idx in range(SAVESLOTS):
                            if 'SLOT' + str(
                                    idx) == self.hovered_item and self.hovered_item_previous != self.hovered_item:
                                glob.user_selection = idx
                                user_is_inactive = False
                                self.hovered_item_previous = self.hovered_item
                                break
                        if 'BACK' == self.hovered_item and self.hovered_item_previous != self.hovered_item:
                            glob.user_selection = SAVESLOTS
                            user_is_inactive = False

                elif event.type == pg.MOUSEBUTTONUP:
                    if get_hovered_rectangle(self.clickable_item, event.pos) is not None:
                        user_is_inactive = False
                        self.load_validation_handler()

                elif event.type == pg.KEYDOWN:
                    user_is_inactive = False
                    if event.key == pg.K_ESCAPE:
                        glob.user_selection = SAVESLOTS  # Last menu line is 'BACK'
                        self.load_validation_handler()
                    elif event.key == pg.K_DOWN:
                        glob.user_selection += 1
                        if glob.user_selection > SAVESLOTS:
                            glob.user_selection = 0
                    elif event.key == pg.K_UP:
                        glob.user_selection -= 1
                        if glob.user_selection < 0:
                            glob.user_selection = SAVESLOTS
                    elif event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        self.load_validation_handler()

            if user_is_inactive:
                pg.time.wait(SLEEPTIME)

    def load_validation_handler(self):
        """ Processes the exit from the load menu.

        :return: None
        """

        if glob.user_selection >= SAVESLOTS:
            glob.active_screen = "mainmenu"
            glob.user_selection = 0
        elif glob.saved_games[glob.user_selection]['timestamp'] > datetime.min:
            if DEBUG:
                print("Loading SLOT" + str(glob.user_selection), glob.saved_games[glob.user_selection])
            self.game_params = glob.saved_games[glob.user_selection]['game_params']
            glob.active_screen = "capytaine"
            glob.user_selection = 0
