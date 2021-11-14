"""
    This module builds the screen to display to the user once in game.

    Class
    -----
    GameDisplay:
        a class used to draw the screen to display
"""

import pygame as pg
from datetime import datetime

import globvars as glob
from capylib import draw_text, get_nbr_lines, draw_multilines_text
from sprites import Player, NPC
from story import QuestType1, QuestType2
from settings import *


class GameDisplay:
    """
        A class used to draw the screen to display,
        a singleton class.

        Attributes
        ----------
        game: Game
            the 'Game' object from which this class was instantiated

        Methods
        -------
        draw_game(self):
            function that builds the screen to display when in game
        show_pause_screen(self):
            displays the pause menu
        show_keys_screen(self):
            displays game keys
        show_save_screen(self):
            displays save menu
        show_quest_screen(self):
            displays quest journal
        show_goals_screen(self):
            displays goals screen or the explanation sheet of the selected goal
        show_medal_screen(self, goal_nbr, is_last_quest):
            displays a medal when a goal is completed
    """

    def __init__(self, game):
        self.whoami = __name__

        self.game = game

        # Surface creation section:
        self.pause_screen = pg.Surface(SIZE, pg.SRCALPHA)
        self.pause_screen.fill((0, 0, 0, 120))

        self.quest_journal_screen = pg.image.load(IMAGEDIR + 'parchment.png')  # Surface((17 * TILESIZE, 12 * TILESIZE), pg.SRCALPHA)
        self.quest_journal_screen_rect = self.quest_journal_screen.get_rect()
        self.quest_journal_screen_rect.center = glob.screen.get_rect().center

        self.goal_selection = pg.Surface((766, 145))
        self.goal_selection_rect = self.goal_selection.get_rect()
        self.goal_selection_rect.center = (WIDTH / 2, HEIGHT / 2)

        self.toolbar = pg.Surface((WIDTH, TILESIZE))
        self.toolbar_rect = self.toolbar.get_rect()
        self.toolbar_rect.topleft = (0, 0)

        self.map_screen = pg.Surface(SIZE)
        self.map_screen_rect = self.map_screen.get_rect()
        self.map_screen_rect.topleft = (0, 0)

        self.text_box = pg.Surface((WIDTH, 2 * TILESIZE))
        self.text_box_rect = self.text_box.get_rect()
        self.text_box_rect.bottomleft = (0, HEIGHT)

        # Images:
        self.quest_mark_black = pg.image.load(IMAGEDIR + 'questMark_black.png').convert_alpha()
        self.quest_mark_grey = pg.image.load(IMAGEDIR + 'questMark_grey.png').convert_alpha()
        self.quest_mark_green = pg.image.load(IMAGEDIR + 'questMark_green.png').convert_alpha()
        self.medal_img = pg.transform.scale2x(pg.image.load(IMAGEDIR + 'medal.png').convert_alpha())
        self.down_arrow = pg.image.load(IMAGEDIR + 'down_arrow.png').convert_alpha()
        self.up_arrow = pg.image.load(IMAGEDIR + 'up_arrow.png').convert_alpha()
        self.locked_img = pg.image.load(IMAGEDIR + 'locked.png').convert_alpha()
        self.goal_medal_img = pg.image.load(IMAGEDIR + 'goal_medal.png').convert_alpha()
        self.keyboard_img = pg.image.load(IMAGEDIR + 'keyboard.png').convert_alpha()
        self.over_text_box_img = pg.image.load(IMAGEDIR + 'over_text_box.png').convert_alpha()
        self.savemenu_bkg = pg.image.load(IMAGEDIR + 'bkg-swirls.jpg')
        self.select_right = pg.image.load(IMAGEDIR + 'select_right.png')
        self.select_left = pg.image.load(IMAGEDIR + 'select_left.png')

    def draw_game(self):
        """ Function that builds the screen to display when in game.

        Draw the map, sprites, quest mark, tool and text box.

        !!! It's important to 'blit' each section on the screen. !!!

        :return: None
        """

        glob.screen.fill(BLACK)  # Start from a blank page ;)

        # Draw the map:
        self.map_screen.fill(BLACK)
        self.map_screen.blit(self.game.map.image, self.game.camera.apply(self.game.map.rect))

        # Draw all sprites:
        for sprite in self.game.all_sprites:
            if sprite.name not in self.game.removed_objects:
                sprite_image = sprite.get_image()
                assert isinstance(sprite_image, pg.Surface), "{} image is not a Surface object".format(sprite.name)
                # Player and NPC images are smaller than a tile so we have to center them
                if isinstance(sprite, Player) or isinstance(sprite, NPC):
                    x_offset = (TILESIZE - sprite_image.get_width()) / 2
                    y_offset = (TILESIZE - sprite_image.get_height()) / 2
                else:
                    x_offset = 0
                    y_offset = 0
                x = self.game.camera.apply(sprite).x
                y = self.game.camera.apply(sprite).y

                self.map_screen.blit(sprite_image, (x + x_offset, y + y_offset))

        # Draw quest mark on npc:
        if self.game.script.current_quest.state == 1:  # quest is unlocked but not accepted yet
            quest_mark_image = self.quest_mark_black
            for c in self.game.characters:
                if c.name == self.game.script.current_quest.quest_giver_name:
                    quest_mark_image_rect = quest_mark_image.get_rect()
                    quest_mark_image_rect.topleft = (c.x * TILESIZE, (c.y - 1) * TILESIZE)
                    self.map_screen.blit(quest_mark_image, self.game.camera.apply(quest_mark_image_rect))
        elif self.game.script.current_quest.state == 2:  # quest is in progress but not completed yet
            if isinstance(self.game.script.current_quest, QuestType2) and not self.game.script.current_quest.validated:
                quest_mark_image = self.quest_mark_grey
            else:
                quest_mark_image = self.quest_mark_green

            for c in self.game.characters:
                if c.name == self.game.script.current_quest.quest_validator_name:
                    quest_mark_image_rect = quest_mark_image.get_rect()
                    quest_mark_image_rect.topleft = (c.x * TILESIZE, (c.y - 1) * TILESIZE)
                    self.map_screen.blit(quest_mark_image, self.game.camera.apply(quest_mark_image_rect))

        # End of map section => blit map:
        glob.screen.blit(self.map_screen, self.map_screen_rect)

        # Draw text box:
        if self.game.player.interacting:
            self.text_box.fill(BLACK)

            npc = self.game.player.interact_with_npc()
            obj = self.game.player.interact_with_object()

            if npc is not None:
                dialogue = self.game.script.get_dialogue(npc.name)
            elif obj is not None:
                dialogue = self.game.script.get_dialogue(obj.type[0:-1])
            else:
                dialogue = None

            self.game.nbr_lines = get_nbr_lines(WIDTH - TILESIZE, dialogue, 25, (5,0), self.text_box)
            text_surface = pg.Surface((WIDTH - TILESIZE, self.game.nbr_lines * TILESIZE))  # WIDTH - TILESIZE to let space for arrow images
            text_rect = text_surface.get_rect()
            text_rect.topleft = (0, - self.game.line_number*TILESIZE)
            draw_multilines_text(text_surface, text_rect, dialogue, coordinate=(5,0), surface=self.text_box)

            glob.screen.blit(self.text_box, self.text_box_rect)
            glob.screen.blit(self.over_text_box_img, (0, self.text_box_rect.y - 2 * TILESIZE))

            if self.game.line_number > 0:
                glob.screen.blit(self.up_arrow, (WIDTH - TILESIZE, HEIGHT - 2*TILESIZE))

            if self.game.line_number < self.game.nbr_lines - 1:
                glob.screen.blit(self.down_arrow, (WIDTH - TILESIZE, HEIGHT - TILESIZE))

        elif self.game.player.ready_to_interact():
            draw_text(self.game, "Appuie sur la barre espace pour intéragir", 25, self.text_box_rect.midtop, "midtop")

        # Draw tools:
        tool_image = self.game.inventory.get_tool_image()
        if tool_image is not None:
            tool_image_rect = tool_image.get_rect()
            tool_image_rect.topleft = (WIDTH - TILESIZE, HEIGHT - TILESIZE)

            glob.screen.blit(tool_image, tool_image_rect)

    # SCREENS SECTION:
    def show_pause_screen(self):
        """ Displays the pause menu.

        :return: None
        """

        self.game.clickable_item = {}
        glob.screen.blit(self.pause_screen, (0, 0))

        for idx in range(len(PAUSEMENU_ITEMS)):
            text = PAUSEMENU_ITEMS[idx][1]

            # Special case management:
            if PAUSEMENU_ITEMS[idx][0] == "musicmode":
                text += " : " + ("On" if glob.user_config["music_on"] else "Off")

            if glob.user_selection != idx:
                fontsize = 25
            else:
                fontsize = 30
                font = pg.font.Font(pg.font.match_font(DEFAULTFONT), fontsize)
                text_surface = font.render(' ' + text + ' ', True, BLACK)
                text_width = text_surface.get_width()
                position_left = (WIDTH / 2 - text_width / 2 - TILESIZE, HEIGHT / 2 - 147 + idx * 50)
                position_right = (WIDTH / 2 + text_width / 2, HEIGHT / 2 - 147 + idx * 50)

                glob.screen.blit(self.select_left, position_left)
                glob.screen.blit(self.select_right, position_right)

            position = (WIDTH/2, HEIGHT/2 - 150 + idx*50)
            draw_text(self.game, text, fontsize, position, "midtop", WHITE, PAUSEMENU_ITEMS[idx][0])

        pg.display.flip()

        if DEBUG:
            print("Pause menu page refreshed at", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def show_keys_screen(self):
        """ Displays game keys.

        :return: None
        """

        glob.screen.blit(self.pause_screen, (0, 0))

        keyboard_rect = self.keyboard_img.get_rect()
        keyboard_rect.center = (WIDTH / 2, HEIGHT / 2)

        glob.screen.blit(self.keyboard_img, keyboard_rect)

    def show_save_screen(self):
        """ Displays save menu.

        :return: None
        """

        self.game.clickable_item = {}
        glob.screen.fill(BLACK)
        glob.screen.blit(self.savemenu_bkg, (0, 0))

        draw_text(self.game, "Sauvegarder la partie", 25, (WIDTH / 2, 60), "midtop", DARKGREY)

        for idx in range(SAVESLOTS):
            if glob.saved_games[idx]['timestamp'] > datetime.min:
                if glob.user_selection != idx:
                    fontsize = 20
                    color = BROWN
                else:
                    fontsize = 25
                    color = RED
                draw_text(self.game, glob.saved_games[idx]['timestamp'].strftime("%m/%d/%Y, %H:%M:%S"), fontsize,
                          (WIDTH / 2, HEIGHT / 2 - 200 + (idx * 50)), "midtop", color, 'SLOT' + str(idx))
            else:
                draw_text(self.game, "VIDE", 20, (WIDTH / 2, HEIGHT / 2 - 200 + (idx * 50)), "midtop",
                          BROWN if glob.user_selection != idx else GREEN, 'SLOT' + str(idx))

        draw_text(self.game, "RETOUR", 20, (WIDTH / 2, HEIGHT / 2 - 200 + (SAVESLOTS * 50)), "midtop",
                  DARKGREY if glob.user_selection < SAVESLOTS else GREEN, 'BACK')

        pg.display.flip()
        if DEBUG:
            print("Save page refreshed at", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def show_quest_screen(self):
        """ Displays quest journal.

        :return: None
        """

        quest = self.game.script.current_quest
        glob.screen.blit(self.pause_screen, (0, 0))
        rect = self.quest_journal_screen_rect
        glob.screen.blit(self.quest_journal_screen, rect.topleft)

        # Draw goal title:
        pos = (rect.topleft[0] + TILESIZE, rect.topleft[1] + TILESIZE)
        if quest.state == 2:
            goal_title = self.game.script.all_goals[quest.goal_nbr].title
        else:
            goal_title = self.game.script.all_goals[0].title

        draw_text(self.game, "ODD: " + goal_title, 20, pos, "topleft", BLACK)

        # Draw the mission in the center of the quest journal:
        if quest.state == 2:
            image = quest.quest_validator_image
            if isinstance(quest, QuestType1):
                draw_text(self.game, quest.statement, 25, rect.center, "center", BLACK)
            elif isinstance(quest, QuestType2):
                objectif = "   (" + str(quest.current_obj_nbr) + "/" + str(quest.obj_nbr) + ")"
                draw_text(self.game, quest.statement + objectif, 25, rect.center, "center", BLACK)
                if not quest.validated:
                    image = quest.obj_image

            image_rect = image.get_rect()
            image_rect.center = (rect.center[0], rect.center[1] + 2 * TILESIZE)
            glob.screen.blit(image, image_rect)
        else:
            draw_text(self.game, "Pas de mission en cours", 25, rect.center, "center", BLACK)

        # Draw the link to the goals screen:
        if self.game.inventory.goals_booklet_acquired:
            pos = (rect.bottomright[0] - TILESIZE, rect.bottomright[1] - TILESIZE)
            if quest.state == 2:
                draw_text(self.game, "Appuie sur G pour découvrir l'objectif lié à cette mission", 20, pos, "bottomright", BLACK)
            else:
                draw_text(self.game, "Appuie sur G pour ouvrir la liste des ODD", 20, pos, "bottomright", BLACK)

    def show_goals_screen(self):
        """ Displays goals screen or the explanation sheet of the selected goal.

        :return: None
        """

        glob.screen.blit(self.pause_screen, (0, 0))

        i = self.game.script.current_goal_index + glob.user_selection
        goals = self.game.script.all_goals

        if self.game.show_goal:
            goals[i].generate_sheet()

            arrow_rect = self.down_arrow.get_rect()  # same rect size for up and down arrow
            if i > 0:
                arrow_rect.midtop = (WIDTH / 2, 0)
                glob.screen.blit(self.up_arrow, arrow_rect)
                draw_text(self.game, "Objectif " + str(i - 1), 20, arrow_rect.midright, "midleft")
            if i < len(goals) - 1:
                arrow_rect.midbottom = (WIDTH / 2, HEIGHT)
                glob.screen.blit(self.down_arrow, arrow_rect)
                draw_text(self.game, "Objectif " + str(i + 1), 20, arrow_rect.midright, "midleft")

        else:
            for g in range(len(goals)):
                if g == i - 1:
                    goals[g].generate_card((WIDTH / 2, (HEIGHT / 2) - (5 * TILESIZE)))
                elif g == i:
                    self.goal_selection.fill(goals[g].color)
                    glob.screen.blit(self.goal_selection, self.goal_selection_rect)
                    goals[g].generate_card((WIDTH / 2, HEIGHT / 2))
                    draw_text(self.game, "Appuie sur la barre espace pour découvrir l'objectif", 20, (WIDTH / 2,HEIGHT/2 + 1.5*TILESIZE), "midtop")
                elif g == i + 1:
                    goals[g].generate_card((WIDTH / 2, (HEIGHT / 2) + (5 * TILESIZE)))

            arrow_rect = self.down_arrow.get_rect()  # same rect size for up and down arrow
            if i > 1:
                arrow_rect.center = (WIDTH / 2, TILESIZE)
                image = pg.transform.scale2x(self.up_arrow)
                glob.screen.blit(image, arrow_rect)
            if i < len(goals) - 2:
                arrow_rect.center = (WIDTH / 2, HEIGHT - 2*TILESIZE)
                image = pg.transform.scale2x(self.down_arrow)
                glob.screen.blit(image, arrow_rect)

    def show_medal_screen(self, goal_nbr, is_last_quest):
        """ Displays a medal when a goal is completed.

        :param goal_nbr: number of completed goal, the second element in 'game.show_medal' tuple
        :param is_last_quest: True if last quest, the third element in game.show_medal' tuple
        :return: None
        """

        glob.screen.blit(self.pause_screen, (0, 0))

        medal_rect = self.medal_img.get_rect()
        medal_rect.center = (WIDTH / 2, HEIGHT / 2)

        glob.screen.blit(self.medal_img, medal_rect)

        x = medal_rect.x + (medal_rect.w / 2)
        y = medal_rect.y + medal_rect.h + 30
        if is_last_quest:
            draw_text(self.game, "Tu as terminé le jeu, félicitations!", 30, (x, y), "midtop")
            draw_text(self.game, "N'hésite pas à lire les autres ODD en attendant nos prochaines mises à jour.", 25, (x, y + 40), "midtop")
        else:
            draw_text(self.game, "Objectif " + str(goal_nbr) + " complété!", 30, (x, y), "midtop")
            draw_text(self.game, self.game.script.all_goals[goal_nbr].title, 30, (x, y + TILESIZE), "midtop")
