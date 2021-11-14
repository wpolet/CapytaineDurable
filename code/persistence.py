"""
    This module manages saves and recovery of game status.

    Class
    -----
    Persistence
"""

from os import path
from datetime import datetime
import pickle

import globvars as glob
from settings import *


class Persistence:
    """
        A class used to manage saves and recovery of game status.
        Requires installation of pickle module : https://docs.python.org/3.8/library/pickle.html
        Requires definition of constant SAVEPATH in 'settings.py' file.

        Methods
        -------
        save_user_config(self):
            save game config in CONFIGPATH file
        get_saved_games(self):
            read SAVEPATH file to load the list of previously saved games.
        save_this_game(self, game, slot):
            save current game parameters in SAVEPATH file

    """

    def __init__(self):
        # Initialize save slots
        glob.saved_games = [{"timestamp": datetime.min} for idx in range(SAVESLOTS)]

        # Create initial SAVEPATH file if not exists:
        if not path.exists(SAVEPATH):
            with open(SAVEPATH, 'wb') as savefile:
                pickle.dump(glob.saved_games, savefile, pickle.HIGHEST_PROTOCOL)
                savefile.close()

        # Load user config parameters from CONFIGPATH file:
        if path.exists(CONFIGPATH):
            with open(CONFIGPATH, 'rb') as configfile:
                glob.user_config = pickle.load(configfile)
                configfile.close()

    def save_user_config(self):
        """ Save game config in CONFIGPATH file.

        :return: None
        """

        with open(CONFIGPATH, 'wb') as configfile:
            pickle.dump(glob.user_config, configfile, pickle.HIGHEST_PROTOCOL)
            configfile.close()

    def get_saved_games(self):
        """ Read SAVEPATH file to load the list of previously saved games.

        :return: None
        """

        with open(SAVEPATH, 'rb') as savefile:
            glob.saved_games = pickle.load(savefile)
            savefile.close()

        # Ensure file structure matches SAVESLOTS setting
        if len(glob.saved_games) > SAVESLOTS:
            glob.saved_games = glob.saved_games[0:SAVESLOTS]
        elif len(glob.saved_games) < SAVESLOTS:
            glob.saved_games += [{"timestamp": datetime.min} for idx in range(len(glob.saved_games), SAVESLOTS)]

    def save_this_game(self, game, slot):
        """ Save current game parameters in SAVEPATH file.

        :param game: Game object
        :param slot: save slot selected by the user
        :return: list of all saved games
        """

        glob.saved_games[slot] = {
            "timestamp": datetime.now(),
            # !!! The game_params variable must have the same structure as GAME_STARTUP_PARAMS !!!
            "game_params": {
                "player": {
                    "name": game.player.name,
                    "x": game.player.x,
                    "y": game.player.y,
                    "look_at": game.player.look_at
                },
                "map": {
                    "name": game.map.name
                },
                "maps_version": game.script.maps_version,
                "unlocked_tools": {
                    "axe": game.inventory.axe.acquired,
                    "shovel": game.inventory.shovel.acquired,
                    "pickaxe": game.inventory.pickaxe.acquired,
                    "net": game.inventory.net.acquired
                },
                "current_quest": {
                    "name": game.script.current_quest.name,
                    "state": game.script.current_quest.state,
                    "current_obj_nbr": game.script.current_quest.current_obj_nbr
                },
                "quest_journal_acquired": game.inventory.quest_journal_acquired,
                "goals_booklet_acquired": game.inventory.goals_booklet_acquired,
                "removed_objects": game.removed_objects
            }
        }

        # Sort array by timestamp
        glob.saved_games.sort(key=lambda item: item['timestamp'], reverse=True)

        # Commit to disk
        with open(SAVEPATH, 'wb') as savefile:
            pickle.dump(glob.saved_games, savefile, pickle.HIGHEST_PROTOCOL)
            savefile.close()

        # Return updated list
        return glob.saved_games
