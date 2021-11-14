"""
    This module manages the creation and use of all tools.

    Class
    -----
    Inventoy:
        A class used to manage all tools
    Tool:
        A class used to materialize player's tools
        subclasses: Axe, Shovel, Pickaxe, Net
"""

import pygame as pg

from settings import *


class Inventory:
    """
        A class used to manage all tools,
        a singleton class.

        Attributes
        ----------
        game: Game
            the 'Game' object from which this class was instantiated
        tools: list of Tool object
            list containing all tools instance
        axe, shovel, pickaxe, net: Tool
            tools instance
        quest_journal_acquired, goals_booklet_acquired:
            set to 'true' according to the progress of the scenario
            allows to display or not the corresponding screen

        Methods
        -------
        tool_to_use(self, typeObj):
            returns the tool to use according to the type of the object
        grab(self, key):
            set 'in_hand' tool's attribute to True and False for the other tools
        drop_tool(self):
            drop any tool the player may have in hand
        ready_to_use(self, typeObj):
            returns True if the player has acquired the tool and has it in hand, False otherwise
        get_tool_image(self):
            returns the image of the object whose attribute 'in_hand' is true
    """

    def __init__(self, game):
        self.game = game

        self.tools = []

        # Tools:
        self.axe = Tool(self, "axe", "Tu as besoin d'une hache pour ça ;)", pg.K_c)
        self.shovel = Tool(self, "shovel", "Tu as besoin d'une pelle pour ça ;)", pg.K_v)
        self.pickaxe = Tool(self, "pickaxe", "Tu as besoin d'une pioche pour ça ;)", pg.K_b)
        self.net = Tool(self, "net", "Tu as besoin d'un filet pour ça ;)", pg.K_n)

        # Quest & goals screen:
        self.quest_journal_acquired = game.game_params["quest_journal_acquired"]
        self.goals_booklet_acquired = game.game_params["goals_booklet_acquired"]

    def tool_to_use(self, obj_type):
        """ Returns the tool to use according to the type of the object.

        :param obj_type: 'type' attribute of the object
        :return: a tool object
        """

        assert isinstance(obj_type, str), "npc_name must be a string"
        if obj_type == "tree":
            return self.axe
        elif obj_type == "dirt":
            return self.shovel
        elif obj_type == "rock":
            return self.pickaxe
        elif obj_type == "trash":
            return self.net
        else:
            return None

    def grab(self, key):
        """ Set 'in_hand' attribute to True and False for the other tools
            or set to False if it is True.

        The 'key' parameter comes from the 'events' method in Game class.
        Each tool has a 'key' attribute to compare.

        :param key: a pygame event, the key pressed by the user
        :return: None
        """

        for tool in self.tools:
            if key == tool.key and tool.acquired:
                tool.in_hand = not tool.in_hand
            else:
                tool.in_hand = False

    def drop_tool(self):
        """ Drop any tool the player may have in hand.

        :return: None
        """

        for tool in self.tools:
            tool.in_hand = False

    def ready_to_use(self, obj_type):
        """ Returns True if the player has acquired the tool and has it in hand, False otherwise.

        :param obj_type: 'type' attribute of the object
        :return: True if the player has acquired the tool and has it in hand, False otherwise
        """

        tool = self.tool_to_use(obj_type)
        if tool is not None:
            if not (tool.acquired and tool.in_hand):  # If he has neither acquired nor in hand the tool he cannot use it
                return False
        return True

    def get_tool_image(self):
        """ Returns the image of the object whose attribute 'in_hand' is true.

        Thanks to this function, 2 tools cannot have their 'in_hand' attribute True at the same time.

        :return: the tool image to display
        """

        if self.pickaxe.in_hand:
            return self.pickaxe.image
        elif self.axe.in_hand:
            return self.axe.image
        elif self.net.in_hand:
            return self.net.image
        elif self.shovel.in_hand:
            return self.shovel.image
        else:
            return None


class Tool:
    """
        A class used to materialize player's tools,

        Attributes
        ----------
        name: str
            the tool name
        image: Image
            the image to display for this tool
        use_text: str
            text displayed when inventory.ready_to_use == false
        key: pygame key
            pygame key linked to this tool
        acquired: bool
            variable indicating whether the tool is acquired or not
        in_hand: bool
            variable indicating whether the tool is in player's hands or not
    """

    def __init__(self, inventory, name, use_text, key):
        self.name = name
        self.image = pg.image.load(IMAGEDIR + 'tools/' + self.name + '.png').convert_alpha()
        self.use_text = use_text
        self.key = key

        self.acquired = inventory.game.game_params["unlocked_tools"][name]
        self.in_hand = False

        inventory.tools.append(self)
