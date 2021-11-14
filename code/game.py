"""
    This module manages the creation and use of all tools.

    Class
    -----
    Game:

"""

import pygame as pg
from os import path
from datetime import datetime

import globvars as glob
from capylib import draw_text, get_hovered_rectangle, exit_gracefully
from game_display import GameDisplay
from sprites import Player, Obstacle, NPC, Object, Gate
from story import Script, QuestType2
from tilemap import TiledMap, Camera
from inventory import Inventory
from settings import *


class Game:
    """
        Main class to manage the game.

        Attributes
        ----------
        game_params: dictionary
            saved game parameters or default parameters from 'settings.py'
        hovered_item: dictionary ID of Rect object
            Holds id of rectangle currently hovered by mouse pointer
        hovered_item_previous: dictionary ID of Rect object
            Holds id of last hovered rectangle to allow detection of state changes
        clickable_item: dictionary of Rect object
            contains all rectangles that must react to mouse events
        line_number: int
            an increment for sentences of interaction texts
        nbr_lines: int
            the number of lines of text to display in text box

        paused, show_keys, show_save, show_quest, show_goals, show_goal, show_medal: bool
            Boolean variables to know what to display on the screen

        game_display, player, map, camera, script, inventory: objects
            instantiation of classes of the same name

        all_sprites, obstacles, characters, objects, gates: sprites group
            groups for sprites created in 'sprites.py'

        removed_objects: list of strings
            keeps the name of removed objects not to reload them

        Methods
        -------
        load_map(self, to_map_name, from_map_name=None):
            creates the TiledMap object and all sprites objects on it
        display(self):
            call display functions based on boolean variables
        game_events(self):
            manages user actions in the game
        pause_menu_validation_handler(self):
            processes the exit from the pause menu
        save_validation_handler(self):
            processes the exit from the save menu
        interact(self):
            manages the interactions between the player and the characters and objects
        update(self):
            Updates the position and presence of game elements and camera
    """

    _instance = None

    def __new__(cls, dummy):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, game_params):
        self.whoami = __name__

        # Pygame setup:
        pg.key.set_repeat(KEYREPEATDELAY, KEYREPEATINTERVAL)
        pg.mouse.set_visible(False)

        # Variables:
        self.game_params = game_params
        self.hovered_item = None  # Holds id of rectangle currently hovered by mouse pointer
        self.hovered_item_previous = None  # Holds id of last hovered rectangle to allow detection of state changes
        self.clickable_item = {}  # contains all rectangles that must react to mouse events
        self.line_number = 0  # Increment for sentences of interaction texts
        self.nbr_lines = 0  # Number of lines of text to display in text box

        # Boolean variables to know what to display:
        self.paused = False  # True when the pause screen is displayed
        self.show_keys = False  # True when the keys screen is displayed
        self.show_save = False  # True when the save screen is displayed
        self.show_quest = False  # True when player wants to see the quest log
        self.show_goals = False  # True when the goals screen is displayed
        self.show_goal = False  # True when the goal explanation screen is displayed
        self.show_medal = (False, 0, False)  # True at chapter end

        # Sprites groups:
        self.all_sprites = pg.sprite.Group()  # == Player + NPC + Object -> can move or be removed
        self.obstacles = pg.sprite.Group()
        self.characters = pg.sprite.Group()
        self.objects = pg.sprite.Group()
        self.gates = pg.sprite.Group()

        self.removed_objects = self.game_params["removed_objects"]  # keeps the name of removed objects in order to discard them at reload time

        # Music:
        if path.exists(SONGPATH):
            pg.mixer.music.load(SONGPATH)
            pg.mixer.music.set_volume(0.1)

            if glob.user_config["music_on"]:
                pg.mixer.music.play(-1)  # -1: the music will repeat indefinitely

        # Game objects:
        self.game_display = GameDisplay(self)
        self.player = Player(self, self.game_params["player"]['x'], self.game_params["player"]['y'])
        self.map = None  # instantiated in 'load_map' function
        self.camera = None  # instantiated in 'load_map' function
        self.script = Script(self)
        self.inventory = Inventory(self)

        # Cheat code:
        self.show_cheat_box = False
        self.input_box = pg.Surface((85, 30))
        self.input_box_rect = self.input_box.get_rect()
        self.cheat_text = ""

        # Load default map from 'settings.py' or saved map:
        self.load_map(game_params["map"]["name"])

    def load_map(self, to_map_name, from_map_name=None):
        """ Creates the TiledMap object and all sprites objects on it.

        the 'from_map_name' parameter is given when the player enters a new map,
        this allows you to simply modify the player position to match map entry
        according to the source map.

        /!\ Player is a created in self.__init__ function, 'load_map' just changes its x & y attributes

        :param to_map_name: destination map to load
        :param from_map_name: the source map used to place the player on the new map
        :return: None
        """

        self.map = TiledMap(self, to_map_name)

        # Reset groups:
        self.all_sprites.empty()
        self.obstacles.empty()
        self.characters.empty()
        self.objects.empty()
        self.gates.empty()

        # Each object in Tiled Map editor has the following properties:
        # name, type, x, y, width, height used to create game objects
        # !!! x & y are in pixels
        for obj in self.map.tmxdata.objects:
            if obj.type == "gate":
                Gate(self, obj.x, obj.y, obj.width, obj.height, obj.name, obj.dx, obj.dy)
                if obj.name == from_map_name:  # places the player at the entrance
                    self.player.x = obj.x/TILESIZE
                    self.player.y = obj.y/TILESIZE
            elif obj.type[0:3] == "npc":
                NPC(self, obj.x, obj.y, obj.width, obj.height, obj.name, obj.type, obj.look_to)
            elif obj.type[0:-1] in ["tree", "dirt", "rock", "trash"]:
                if obj.name not in self.removed_objects:
                    Object(self, obj.x, obj.y, obj.width, obj.height, obj.name, obj.type)
            elif obj.type == "obstacle":
                Obstacle(self, obj.x, obj.y, obj.width, obj.height)

        self.all_sprites.add(self.player)  # keep the same object Player

        self.camera = Camera(self.map.width, self.map.height)

        pg.event.clear()

    # EXECUTION SECTION:
    def display(self):
        """ Call display functions based on boolean variables.

        :return: None
        """

        # Pause and medal screen are transparent => draw first the game screen behind
        self.game_display.draw_game()

        # Draw pause screen:
        if self.paused:
            self.game_display.show_pause_screen()

        # Draw keys screen:
        if self.show_keys:
            self.game_display.show_keys_screen()

        # Draw save screen:
        if self.show_save:
            self.game_display.show_save_screen()

        # Draw quest journal screen:
        if self.show_quest:
            self.game_display.show_quest_screen()

        # Draw goals screen:
        if self.show_goals:
            self.game_display.show_goals_screen()

        # Draw medal at chapter end:
        if self.show_medal[0]:
            self.game_display.show_medal_screen(self.show_medal[1], self.show_medal[2])


        # Draw cheat box:
        if self.show_cheat_box:
            glob.screen.blit(self.input_box, self.input_box_rect)
            draw_text(self, self.cheat_text, 25, self.input_box_rect.topleft)

        # Once everything is drawn the screen displayed:
        pg.display.flip()

        if DEBUG:
            print("Game screen refreshed at", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def game_events(self):
        """ Manages user actions in the game.

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
                        if self.paused:
                            for idx in range(len(PAUSEMENU_ITEMS)):
                                if PAUSEMENU_ITEMS[idx][0] == self.hovered_item and self.hovered_item_previous != self.hovered_item:
                                    glob.user_selection = idx
                                    user_is_inactive = False
                                    self.hovered_item_previous = self.hovered_item
                                    break

                        elif self.show_save:
                            for idx in range(SAVESLOTS):
                                if 'SLOT' + str(idx) == self.hovered_item and self.hovered_item_previous != self.hovered_item:
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
                        if self.paused:
                            self.pause_menu_validation_handler()
                        elif self.show_save:
                            self.save_validation_handler()

                elif event.type == pg.KEYDOWN:
                    user_is_inactive = False

                    # Pause screen events:
                    if self.paused:
                        if event.key == pg.K_ESCAPE:
                            self.paused = False
                            pg.mouse.set_visible(False)
                            pg.key.set_repeat(KEYREPEATDELAY, KEYREPEATINTERVAL)
                            glob.user_selection = 0
                        elif event.key == pg.K_DOWN:
                            glob.user_selection += 1
                            if glob.user_selection >= len(PAUSEMENU_ITEMS):
                                glob.user_selection = 0
                        elif event.key == pg.K_UP:
                            glob.user_selection -= 1
                            if glob.user_selection < 0:
                                glob.user_selection = len(PAUSEMENU_ITEMS) - 1
                        elif event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                            self.pause_menu_validation_handler()

                    # Keys screen events:
                    elif self.show_keys:
                        if event.key == pg.K_ESCAPE or event.key == pg.K_SPACE:
                            self.show_keys = False
                            pg.key.set_repeat(KEYREPEATDELAY, KEYREPEATINTERVAL)
                            glob.user_selection = 0

                    # Save screen events:
                    elif self.show_save:
                        if event.key == pg.K_ESCAPE:
                            glob.user_selection = SAVESLOTS  # Last menu line is 'BACK'
                            self.save_validation_handler()
                        elif event.key == pg.K_DOWN:
                            glob.user_selection += 1
                            if glob.user_selection > SAVESLOTS:
                                glob.user_selection = 0
                        elif event.key == pg.K_UP:
                            glob.user_selection -= 1
                            if glob.user_selection < 0:
                                glob.user_selection = SAVESLOTS
                        elif event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                            self.save_validation_handler()

                    # Quest screen events:
                    elif self.show_quest:
                        if event.key == pg.K_ESCAPE or event.key == pg.K_SPACE or event.key == pg.K_f:
                            self.show_quest = False
                        elif event.key == pg.K_g:
                            self.show_quest = False
                            self.show_goals = True

                    # Goals screen events:
                    elif self.show_goals:
                        if event.key == pg.K_ESCAPE or event.key == pg.K_g:
                            if self.show_goal:
                                self.show_goal = False
                            else:
                                self.show_goals = False
                                pg.key.set_repeat(KEYREPEATDELAY, KEYREPEATINTERVAL)
                                glob.user_selection = 0
                        elif event.key == pg.K_UP:
                            if glob.user_selection + self.script.current_goal_index > 0:
                                glob.user_selection -= 1
                        elif event.key == pg.K_DOWN:
                            if glob.user_selection + self.script.current_goal_index < len(self.script.all_goals) - 1:
                                glob.user_selection += 1
                        elif event.key == pg.K_SPACE:
                            self.show_goal = not self.show_goal

                    # Medal screen events:
                    elif self.show_medal[0]:
                        if event.key == pg.K_ESCAPE or event.key == pg.K_SPACE:
                            self.show_medal = (False, self.show_medal[1])

                    # Cheat box events:
                    elif self.show_cheat_box:
                        if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                            self.cheat(self.cheat_text)
                            self.show_cheat_box = False
                            self.cheat_text = ''
                        elif event.key == pg.K_ESCAPE:
                            self.show_cheat_box = False
                            self.cheat_text = ''
                        elif event.key == pg.K_BACKSPACE:
                            self.cheat_text = self.cheat_text[:-1]
                        else:
                            self.cheat_text += event.unicode

                    # In game events:
                    else:
                        if not self.player.interacting:
                            # Player's movements:
                            if event.key == pg.K_LEFT or event.scancode == 30:
                                self.player.move(dx=-1)
                            elif event.key == pg.K_RIGHT or event.scancode == 32:
                                self.player.move(dx=1)
                            elif event.key == pg.K_UP or event.scancode == 17:
                                self.player.move(dy=-1)
                            elif event.key == pg.K_DOWN or event.scancode == 31:
                                self.player.move(dy=1)

                            # Player's actions:
                            elif event.key == pg.K_g:
                                if self.inventory.goals_booklet_acquired:
                                    self.show_goals = True
                                    pg.key.set_repeat()
                            elif event.key == pg.K_f:
                                if self.inventory.quest_journal_acquired:
                                    self.show_quest = True
                            elif event.key in [pg.K_c, pg.K_v, pg.K_b, pg.K_n]:
                                self.inventory.grab(event.key)

                            # Cheat code:
                            elif event.key == pg.K_p:
                                self.show_cheat_box = True

                        else:
                            if event.key == pg.K_UP:
                                if self.line_number > 0:
                                    self.line_number -= 1
                            if event.key == pg.K_DOWN:
                                self.interact(event.key)

                        # Either player is interacting or not:
                        if event.key == pg.K_SPACE:
                            self.interact(event.key)
                        elif event.key == pg.K_ESCAPE:
                            self.paused = True
                            pg.mouse.set_visible(True)
                            pg.key.set_repeat()

                if user_is_inactive:
                    if self.player.steps % 2 != 0:
                        self.player.steps += 1
                        user_is_inactive = False

                    pg.time.wait(SLEEPTIME)

    def pause_menu_validation_handler(self):
        """ Processes the exit from the pause menu.

        :return: None
        """

        if PAUSEMENU_ITEMS[glob.user_selection][0] == "resume":
            self.paused = False
            pg.mouse.set_visible(False)
            pg.key.set_repeat(KEYREPEATDELAY, KEYREPEATINTERVAL)
            glob.user_selection = 0
        elif PAUSEMENU_ITEMS[glob.user_selection][0] == "savegame":
            self.paused = False
            self.show_save = True
        elif PAUSEMENU_ITEMS[glob.user_selection][0] == "showkeys":
            self.paused = False
            self.show_keys = True
        elif PAUSEMENU_ITEMS[glob.user_selection][0] == "musicmode":
            if glob.user_config['music_on']:
                glob.user_config['music_on'] = False
                pg.mixer.music.stop()
            else:
                glob.user_config['music_on'] = True
                pg.mixer.music.play(-1)
        elif PAUSEMENU_ITEMS[glob.user_selection][0] == "backmenu":
            glob.active_screen = "mainmenu"
            glob.user_selection = 0
            pg.mixer.music.stop()
        elif PAUSEMENU_ITEMS[glob.user_selection][0] == "quitgame":
            exit_gracefully(self)

    def save_validation_handler(self):
        """ Processes the exit from the save menu.

        :return: None
        """

        if glob.user_selection < SAVESLOTS:
            glob.saved_games = glob.persistence.save_this_game(self, glob.user_selection)
            if DEBUG:
                print("Game saved on slot", glob.user_selection)
                print(glob.saved_games)

        self.show_save = False
        pg.key.set_repeat(KEYREPEATDELAY, KEYREPEATINTERVAL)
        glob.user_selection = 0

    def interact(self, key):
        """ Manages the interactions between the player and the characters and objects.

        Dialogues are list of strings but 'draw_text' function takes only one string.
        Which is allowed thanks to the variable 'line_number' (see 'draw' function),
        the value of this variable is managed here.

        :return: None
        """

        npc = self.player.interact_with_npc()
        if npc is not None:
            if self.player.interacting:
                self.line_number += 1
                if self.line_number == self.nbr_lines:  # End of interaction
                    if key == pg.K_SPACE:
                        self.script.check_quest(self.script.current_quest)
                        # !!! important to update before setting 'interacting_with' to False !!!

                        self.player.interacting = False
                        npc.interacting_with = False
                        self.line_number = 0
                        pg.key.set_repeat(KEYREPEATDELAY, KEYREPEATINTERVAL)
                    else:
                        self.line_number -= 1
            else:
                self.player.interacting = True
                npc.interacting_with = True
                self.inventory.drop_tool()
                pg.key.set_repeat()

        obj = self.player.interact_with_object()
        if obj is not None:
            quest_object = False

            # If it's a quest object:
            if isinstance(self.script.current_quest, QuestType2):
                quest = self.script.current_quest
                if obj.type[0:-1] == quest.obj_type and quest.state == 2 and not quest.validated and self.inventory.ready_to_use(obj.type[0:-1]):
                    quest_object = True

            if self.player.interacting:
                self.line_number += 1
                if self.line_number == self.nbr_lines:
                    if key == pg.K_SPACE:
                        self.player.interacting = False
                        self.line_number = 0
                        pg.key.set_repeat(KEYREPEATDELAY, KEYREPEATINTERVAL)

                        if quest_object:
                            self.script.current_quest.current_obj_nbr += 1
                            obj.kill()
                            self.script.check_quest(self.script.current_quest)
                    else:
                        self.line_number -= 1
            else:
                if quest_object:
                    self.removed_objects += [obj.name]
                self.player.interacting = True
                pg.key.set_repeat()

    def cheat(self, text):
        quests = self.script.all_quests
        quests_name = []
        for q in quests:
            quests_name.append(q.name)

        if text in quests_name:
            print("OK")
            for q in quests:
                if q.name == text:
                    self.script.current_quest = q
                    current_quest_index = quests.index(self.script.current_quest)
                    if current_quest_index != len(quests) - 1:
                        self.script.next_quest = quests[quests.index(q) + 1]
                    else:
                        self.script.current_quest.last_quest = True
                        self.script.next_quest = None

                    self.script.current_quest.unlock()

                    break  # Stop looping when reaching the current quest
                else:
                    q.state = 3  # Previous quests are already completed

                    if q.name == "chap2q2":
                        self.script.maps_version["map2"] = "_2"
                    elif q.name == "chap3q2":
                        self.script.maps_version["mapC"] = "_2"
                    elif q.name == "chap4q0":
                        self.script.maps_version["mapD"] = "_2"
                        self.script.maps_version["map1"] = "_2"
                        self.script.maps_version["map2"] = "_3"
                    elif q.name == "chap4q5":
                        self.script.maps_version["mapC"] = "_3"
                        self.script.maps_version["mapD"] = "_3"
                        self.script.maps_version["map4"] = "_2"

            for t in self.inventory.tools:
                t.acquired = True

            self.inventory.quest_journal_acquired = True
            self.inventory.goals_booklet_acquired = True

    def update(self):
        """ Updates the position and presence of game elements and camera.

        :return: None
        """

        self.script.update()
        self.all_sprites.update()
        self.camera.update(self.player)
