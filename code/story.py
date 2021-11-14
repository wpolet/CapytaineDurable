"""
    This module manages the creation and advancement of the game story.

    Class
    -----
    Script:
        a class used to create and manage all quests and goals
    Quest:
        a class used to materialize a quest
    Goal:
        a class used to materialize a goal
"""

import pygame as pg
import data
from capylib import draw_text, get_nbr_lines, draw_multilines_text
import globvars as glob
from settings import *


class Script:
    """
        A class used to create and manage all quests and goals,
        quests and goals are stored in 'data.py' file.

        Attributes
        ----------
        game: Game
            the 'Game' object from which this class was instantiated
        all_goals: list of Goal objects
            list containing all the game goals, each goal is added to this list when it is created
        all_quests: list of Quest objects
            list containing all the game quests, each quest is added to this list when it is created
        current_goal_index:
            the goal index of the current quest, 0 by default
        current_quest: Quest
            the current quest is initialized to the first quest of 'quests' list
        next_quest: Quest
            the quest that follows the current quest in the 'quests' list
        interaction_texts: dict
            dictionary containing the default interaction text of objects and characters
        maps_version:
            dictionary containing the current version of each map

        Methods
        -------
        create_all_quests(self):
            create a Quest object for each quest in 'data.py'
        create_all_goals(self):
            create a Goal object for each goal in 'data.py'
        update(self):
            manages the progress of the quests
        check_quest(self, quest):
            updates quest status based on player actions
        get_dialogue(self, name):
            returns the interaction text of a npc or an object depending on the situation
        unlock_script(self):
            unlock the elements of the script
    """

    def __init__(self, game):
        self.game = game
        self.all_goals = []
        self.all_quests = []

        self.create_all_goals()  # Goals in 'data.py'
        self.create_all_quests()  # Quests in 'data.py'

        self.current_goal_index = 0
        current_quest_name = self.game.game_params["current_quest"]["name"]
        for q in self.all_quests:
            if q.name == current_quest_name:
                self.current_quest = q
                current_quest_index = self.all_quests.index(self.current_quest)
                if current_quest_index != len(self.all_quests) - 1:
                    self.next_quest = self.all_quests[self.all_quests.index(q) + 1]
                else:
                    self.current_quest.last_quest = True
                    self.next_quest = None

                break  # Stop looping when reaching the current quest
            else:
                q.state = 3  # Previous quests are already completed

        self.current_quest.state = self.game.game_params["current_quest"]["state"]
        self.current_quest.unlock()  # For the first quest

        self.current_quest.current_obj_nbr = self.game.game_params["current_quest"]["current_obj_nbr"]
        if isinstance(self.current_quest, QuestType2):
            if self.current_quest.current_obj_nbr == self.current_quest.obj_nbr:
                self.current_quest.validated = True

        self.interaction_texts = data.interaction_texts

        self.maps_version = game.game_params["maps_version"]

    def create_all_quests(self):
        """ Create a Quest object for each quest in 'data.py'.

        :return: None
        """

        for q in data.quests:
            if q["quest_type"] == 2:
                QuestType2(self, q["goal_nbr"], q["name"], q["statement"], q["dialogue"], q["npc1_name"], q["npc2_name"], q["npc2_type"], q["obj_type"], q["obj_nbr"])
            else:
                QuestType1(self, q["goal_nbr"], q["name"], q["statement"], q["dialogue"], q["npc1_name"], q["npc2_name"], q["npc2_type"])

    def create_all_goals(self):
        """ Create a Goal object for each goal in 'data.py'.

        :return: None
        """

        for g in data.goals:
            Goal(self, data.goals.index(g), g["title"], g["expl"], g["advice"], g["facts"], g["color"])

    def update(self):
        """ Manages the progress of the quests.

        When the current quest is completed (state==3)
        we unlock the next_quest and it becomes the new current quest.

        !!! as we change the 'current_quest' object each time its state is 3,
        during the game the state attribute of the 'current_quest' object is never
        equal to 0 or 3, always 1 or 2. !!!

        If the player completed the last quest of a chapter,
        this function tells the Game to display an end of chapter message.

        :return: None
        """

        if self.current_quest.state == 3 and self.next_quest is not None:
        # Next_quest is None when current_quest == last quest
            self.current_quest = self.next_quest
            self.current_quest.unlock()
            current_quest_index = self.all_quests.index(self.current_quest)

            if current_quest_index == len(self.all_quests) - 1:
                self.current_quest.last_quest = True
                self.next_quest = None
            else:
                self.next_quest = self.all_quests[self.all_quests.index(self.current_quest) + 1]

        if self.current_quest.state == 2:
            self.current_goal_index = self.current_quest.goal_nbr
        else:
            self.current_goal_index = 0

    def check_quest(self, quest):
        """ Updates quest status based on player actions.

        Method called in 'self.update' on 'self.current_quest'

        :param quest: the quest to check
        :return: None
        """

        quest_giver = quest.get_npc(quest.quest_giver_name)
        quest_validator = quest.get_npc(quest.quest_validator_name)

        if quest_giver is not None:
            if quest_giver.interacting_with:
                quest.accept()

        if isinstance(quest, QuestType1):
            if quest_validator is not None:
                if quest_validator.interacting_with:
                    quest.complete()

        if isinstance(quest, QuestType2):
            if quest.current_obj_nbr == quest.obj_nbr:
                quest.validated = True

            if quest_validator is not None:
                if quest_validator.interacting_with and quest.validated:
                    quest.complete()

        self.unlock_script(quest)  # !!! call this function before changing current quest !!!

    def get_dialogue(self, name):
        """ Returns the interaction text of a npc or an object depending on the situation.

        quest_dialogue[0] = quest giver dialogue to accept the quest
        quest_dialogue[1] = quest giver dialogue when quest is in progress
        quest_dialogue[2] = quest validator dialogue to complete the quest
        quest_dialogue[3] = object quest dialogue (for QuestType2)

        :param name: the name of the npc or the object the player is interacting with
        :return: the interaction text
        """

        assert isinstance(name, str), "name must be a string"
        npc1 = self.current_quest.quest_giver_name
        npc2 = self.current_quest.quest_validator_name
        state = self.current_quest.state

        if isinstance(self.current_quest, QuestType1):
            if state == 1 and name == npc1:
                return self.current_quest.quest_dialogue[0]
            elif state == 2 and name == npc1:
                return self.current_quest.quest_dialogue[1]
            elif state == 2 and name == npc2:
                return self.current_quest.quest_dialogue[2]
        elif isinstance(self.current_quest, QuestType2):
            if state == 1 and name == npc1:
                return self.current_quest.quest_dialogue[0]
            elif state == 2 and not self.current_quest.validated and name in self.current_quest.obj_type:
                tool = self.game.inventory.tool_to_use(name)
                if tool is not None:
                    if not tool.in_hand:
                        return tool.use_text
                return self.current_quest.quest_dialogue[3]
            elif state == 2 and name == npc1 and not self.current_quest.validated:
                return self.current_quest.quest_dialogue[1]
            elif state == 2 and self.current_quest.validated and name == npc2:
                return self.current_quest.quest_dialogue[2]

        # By default:
        return self.interaction_texts[name]

    def unlock_script(self, quest):
        """ Unlock the elements of the script.

        :param quest: the current quest
        :return: None
        """

        # Unlock quest & goals screen:
        if quest.name == "chap1q0" and quest.state == 2:
            self.game.inventory.quest_journal_acquired = True
        elif quest.name == "chap1q1" and quest.state == 2:
            self.game.inventory.goals_booklet_acquired = True

        # Unlock tools:
        if quest.name == "chap2q0" and quest.state == 2:
            self.game.inventory.axe.acquired = True
        elif quest.name == "chap2q1" and quest.state == 2:
            self.game.inventory.shovel.acquired = True
        elif quest.name == "chap2q2" and quest.state == 2:
            self.game.inventory.pickaxe.acquired = True
        elif quest.name == "chap3q1" and quest.state == 2:
            self.game.inventory.net.acquired = True

        # Unlock maps version:
        if quest.name == "chap2q2" and quest.state == 3:
            self.maps_version["map2"] = "_2"
        elif quest.name == "chap3q2" and quest.state == 3:
            self.maps_version["mapC"] = "_2"
        elif quest.name == "chap4q0" and quest.state == 2:
            self.maps_version["mapD"] = "_2"
            self.maps_version["map1"] = "_2"
            self.maps_version["map2"] = "_3"
        elif quest.name == "chap4q5" and quest.state == 3:
            self.maps_version["mapC"] = "_3"
            self.maps_version["mapD"] = "_3"
            self.maps_version["map4"] = "_2"


class Quest:
    """
        A class used to materialize a quest,
        quests are stored in 'data.py' file.

        Attributes
        ----------
        script: Script
            the 'Script' object from which this class was instantiated
        goal_nbr: int
            the objective index linked to this quest
        name: str
            the quest name
        statement: str
            the quest statement
        quest_giver_name: NPC
            the npc who gives the quest
        quest_validator_name: NPC
            the npc who validates the quest, npc1 and npc2 could be the same NPC object
        quest_dialogue1, 2 & 3: list of str
            npc's dialogue depending on quest state
        state: int
            the quest state:
            0: locked, 1: unlocked, 2: in_progress, 3: completed
        last_quest: bool
            True if this quest is the last of the game

        Methods
        -------
        unlock(self)
            changes quest state from 0 to 1
        accept(self)
            changes quest state from 1 to 2
        complete(self)
            changes quest state from 2 to 3
        get_npc(self, npc_name)
            returns NPC object corresponding to npc_name
    """

    def __init__(self, script, goal_nbr, name, statement, dialogue, npc1, npc2, npc2_type):
        self.script = script
        self.goal_nbr = goal_nbr
        self.name = name
        self.statement = statement
        self.quest_giver_name = npc1
        self.quest_validator_name = npc2
        self.quest_validator_image = pg.image.load(IMAGEDIR + 'npc/' + npc2_type + '_s.png').convert_alpha()

        self.quest_dialogue = dialogue

        self.state = 0
        """
            0) locked: previous task is not completed yet
            1) unlocked: previous task is completed
            2) in_progress:  player accepted the quest
            3) completed : player completed the quest
        """

        self.last_quest = False

        script.all_quests.append(self)
        script.all_goals[goal_nbr].corresponding_quests.append(self)

    def unlock(self):
        if self.state == 0:
            self.state = 1

    def accept(self):
        if self.state == 1:
            self.state = 2
            self.get_npc(self.quest_giver_name).interacting_with = False

    def complete(self):
        if self.state == 2:
            self.state = 3
            self.get_npc(self.quest_validator_name).interacting_with = False

            goal = self.script.all_goals[self.goal_nbr]
            if goal.corresponding_quests.index(self) == len(goal.corresponding_quests) - 1:
                if self.goal_nbr != 0 or self.last_quest:
                    self.script.game.show_medal = (True, self.goal_nbr, self.last_quest)

    def get_npc(self, npc_name):
        """ Returns NPC object corresponding to npc_name.

        Quests only keep quest giver and quest validator name, not the NPC object

        :param npc_name: name attribute of NPC object
        :return: NPC object corresponding to npc_name
        """

        assert isinstance(npc_name, str), "npc_name must be a string"
        for npc in self.script.game.characters:
            if npc.name == npc_name:
                return npc
        return None


class QuestType1(Quest):
    """
        A class inherited from the 'Quest' class.

        A quest with just a quest giver and a quest validator.
        Example: "Go talk to this person"
    """

    def __init__(self, script, goal_nbr, name, statement, dialogue, npc1, npc2, npc2_type):
        Quest.__init__(self, script, goal_nbr, name, statement, dialogue, npc1, npc2, npc2_type)
        self.current_obj_nbr = 0


class QuestType2(Quest):
    """
        A class inherited from the 'Quest' class.

        A quest with a quest giver and a quest validator
        but also a type of object to interact with and
        a number of this object to validate the quest.
        Example: "Destroy 4 rocks"
    """

    def __init__(self, script, goal_nbr, name, statement, dialogue, npc1, npc2, npc2_type, obj_type, obj_nbr):
        Quest.__init__(self, script, goal_nbr, name, statement, dialogue, npc1, npc2, npc2_type)
        self.obj_type = obj_type
        self.obj_nbr = obj_nbr

        self.obj_image = pg.image.load(IMAGEDIR + 'objects/' + obj_type + '1.png').convert_alpha()
        self.current_obj_nbr = 0
        self.object_dialogue = []
        self.validated = False  # Quest is validated when current_obj_nbr == obj_nbr


class Goal:
    """
        A class used to materialize a goal,
        goals are stored in 'data.py' file.

        Attributes
        ----------
        script: Script
            the 'Script' object from which this class was instantiated
        game: Game
            the 'Game' object from which this class was instantiated
        index:
            goal index in 'goals' dictionary in 'data.py' file
        title:
            goal title
        expl:
            goal explanation text
        advice:
            goal daily advice
        facts:
            list of facts
        color:
            the background color of the image used to fill goal sheet
        corresponding_quests:
            list of quests linked to this goal
        image:
            goal image stored in image folder

        The image is used in 'generate_card' and 'generate_sheet' function while
        the explanation and facts surface are only sued in 'generate_sheet' function.

        Methods
        -------
        generate_card(self, x_px, y_px, current_goal=False):
            creates the card to display for each goal
        generate_sheet(self):
            creates the explanation sheet to display for each goal
        get_percentage(self):
            returns quest completion percentage
    """

    def __init__(self, script, index, title, expl, advice, facts, color):
        self.script = script
        self.game = script.game
        self.index = index
        self.title = title
        self.expl = expl
        self.advice = advice
        self.facts = facts
        self.color = color

        self.corresponding_quests = []

        self.state_rect = pg.Rect(0, 0, 50, 50)

        self.image = pg.image.load(IMAGEDIR + 'goals/goal' + str(index) + '.PNG').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (TILESIZE, TILESIZE)
        self.width = self.rect.width
        self.height = self.rect.height

        if index != 0:
            self.explanation_surface = pg.Surface((self.width, 8.5 * TILESIZE))
        else:  # goal0 doesn't need facts_surface
            self.explanation_surface = pg.Surface((self.width, 14.5 * TILESIZE))
        self.explanation_surface.fill(self.color)
        self.explanation_rect = self.explanation_surface.get_rect()
        self.explanation_rect.topleft = self.rect.bottomleft

        self.facts_surface = pg.Surface((self.width, 6 * TILESIZE))
        self.facts_surface.fill(self.color)
        self.facts_rect = self.facts_surface.get_rect()
        self.facts_rect.topleft = self.explanation_rect.bottomleft

        script.all_goals.append(self)

    def generate_card(self, coordinate):
        """ Creates the card to display for each goal.

        :param coordinate: the center of the rect on the screen, type: tuple of (pixel, pixel)
        :return: None
        """

        self.rect.center = coordinate
        glob.screen.blit(self.image, self.rect)

        if self.index != 0:  # Nothing is displayed for goal 0
            self.state_rect.topright = self.rect.topright
            percentage = self.get_percentage()

            if percentage != -1:
                if percentage == 100:
                    glob.screen.blit(self.game.game_display.goal_medal_img, self.state_rect)
                else:
                    draw_text(self.game, str(percentage) + ' %', 25, self.state_rect.topright, "topright")
            # else: percentage == -1 => no quests for this goal

    def generate_sheet(self):
        """ Creates the explanation sheet to display for each goal.

        :return: None
        """

        # Goal card on the top:
        self.rect.topleft = (TILESIZE, TILESIZE)
        glob.screen.blit(self.image, self.rect)

        if self.index == 0:
            glob.screen.blit(self.explanation_surface, self.explanation_rect)
            draw_multilines_text(self.explanation_surface, self.explanation_rect, self.expl, 25, (5, 5), BLACK)
        else:
            # Goal explanation in the middle:
            glob.screen.blit(self.explanation_surface, self.explanation_rect)
            draw_multilines_text(self.explanation_surface, self.explanation_rect, self.expl)

            # Goal advice below the explanation:
            draw_text(self.game, "Au quotidien: " + self.advice, 25, self.explanation_rect.bottomleft, "bottomleft")

            # Goal facts at the bottom of the screen:
            glob.screen.blit(self.facts_surface, self.facts_rect)
            pos = (5, 5)  # starts in the topleft corner but not in (0,0) to have space
            max_height = self.facts_surface.get_size()[1]
            for fact in self.facts:
                nbr_lines = get_nbr_lines(self.facts_surface.get_width(), '-' + fact, 20, pos)
                draw_multilines_text(self.facts_surface, self.facts_rect, '-' + fact, 20, pos)
                pos = (pos[0], pos[1] + (25 * nbr_lines))
                if pos[1] > max_height - 25:  # ' - 25' so the next line to write falls entirely into the surface
                    break

    def get_percentage(self):
        """ Returns quest completion percentage.

        Returns -1 if there is no quest linked to this objective or
        if the first quest is not yet accepted.

        :return: the percentage of the goal
        """

        nbr_quests = len(self.corresponding_quests)
        if nbr_quests == 0:
            return -1
        else:
            if self.corresponding_quests[0].state < 2:
                return -1  # don't display the percentage if the player has not yet accepted the first corresponding quest

            nbr_completed_quests = 0
            for q in self.corresponding_quests:
                if q.state == 3:
                    nbr_completed_quests += 1

            return int((nbr_completed_quests / nbr_quests) * 100)
