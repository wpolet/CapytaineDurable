VERSION = 1.0

# define global execution state
DEBUG = False

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (106, 55, 5)

# game settings:
WIDTH = 800  # 25 * 32
HEIGHT = 640  # 20 * 32
SIZE = (WIDTH, HEIGHT)

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

TITLE = "Capytaine Durable"
KEYREPEATDELAY = 120
KEYREPEATINTERVAL = 120

CONFIGPATH = "capytaine.cfg"
SAVEPATH = "capytaine.save"
SONGPATH = "media/TownTheme.mp3"
IMAGEDIR = "img/"
SLEEPTIME = 30  # ms
SAVESLOTS = 6  # Count of save slots must be between 1 and 8
DEFAULTFONT = "arial"

# GAME default startup parameters
# These parameters are overwritten in case of save reload
# !!! The GAME_STARTUP_PARAMS variables must have the same structure as persistance.savedgames.game_params
GAME_STARTUP_PARAMS = {
    "player": {
        "name": "player0",
        "x": GRIDWIDTH // 2,
        "y": GRIDHEIGHT // 2,
        "look_at": (0, 1)
    },
    "map": {
        "name": "map0"
    },
    "maps_version": {},
    "unlocked_tools": {
        "axe": False,
        "shovel": False,
        "pickaxe": False,
        "net": False
    },
    "current_quest": {
        "name": "chap1q0",
        "state": 0,
        "current_obj_nbr": 0
    },
    "quest_journal_acquired": False,
    "goals_booklet_acquired": False,
    "removed_objects": []
}

# MENUs structure:
MAINMENU_ITEMS = [
    ("startgame", "Nouvelle partie"),
    ("loadgame", "Charger une partie"),
    ("displaymode", "Affichage"),
    ("quitmenu", "Quitter")
]

PAUSEMENU_ITEMS = [
    ("resume", "Reprendre"),
    ("savegame", "Sauvegarder la partie"),
    ("showkeys", "Commandes"),
    ("musicmode", "Musique"),
    ("backmenu", "Retour vers menu"),
    ("quitgame", "Quitter")
]
