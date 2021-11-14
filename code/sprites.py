"""
    This module manages the creation and use of all sprites.
    Sprites are instantiated in the 'load map' game function from objects created in Tiled editor.

    Class
    -----
    Player:
        a class used to represent the player
    Obstacle:
        a class used to materialize the obstacles for the player
    NPC:
        a class used to represent a npc, npc = non-player character
    Object:
        a class used to represent an object
    Gate:
        a class used to materialize the gates for the player
"""

import pygame as pg

from settings import *


class Player(pg.sprite.Sprite):
    """
        A class used to represent the player.

        Attributes
        ----------
        game: Game
            the 'Game' object from which this class was instantiated
        interacting: bool
            variable indicating whether the player is interacting or not
        look_at: (int, int)
            difference between the coordinates of the player and the tile he is looking at
            (0,1): below, (0,-1): above, (1,0): right, (-1,0): left
        steps: int
            an integer variable allowing to display different image of a character when it moves
        name: str
            the object name, used to load images
        z_images, q_images, s_images, d_images: Image
            the image to display depending on where the player looks
        rect: Rect
            the rectangle created from the image
        x, y: int
            the coordinates on the map, the position in pixels divided by TILESIZE to have the tile index

        Methods
        -------
        load_images(self, name):
            load all player images depending on which character the user has chosen
        get_image(self):
            returns the image to display depending on where the player looks
        move(self, dx=0, dy=0):
            changes player x and y attributes
        out_of_bounds(self, dx=0, dy=0):
            returns True if the player would be out of bounds
        collide_with_obstacles(self, dx=0, dy=0):
            returns True if the player would collide with obstacles
        on_gate(self):
            if the player is on a gate, return this Gate object
        enter_gate(self, gate):
            loads a new map if the player enters a gate
        ready_to_interact(self):
            returns True if the player is next to a npc or an object
        interact_with_npc(self):
            returns the NPC object next to which the player is, None otherwise
        interact_with_object(self):
            returns the Object object next to which the player is, None otherwise
        update(self):
            updates the player's rectangle x and y attributes
    """

    _instance = None

    def __new__(cls, game, x, y):
        if cls._instance is None:
            cls._instance = super(Player, cls).__new__(cls)
        return cls._instance

    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.name = self.game.game_params['player']['name']
        self.interacting = False
        self.look_at = self.game.game_params['player']['look_at']
        self.steps = 0

        self.z_images = self.q_images = self.s_images = self.d_images = []
        self.load_images()

        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)

        self.x = x
        self.y = y

    def __repr__(self):
        return "<%s sprite (in %d groups) - ID: %d>" % (self.__class__.__name__, len(self.groups), self.game.choice_selected)

    def load_images(self):
        """ Load all player images depending on which character the user has chosen.

        There are 12 images per character, 3 for each direction he can look.
        Z = up, Q = left, S = down and D = right
        *_img = neutral position, *_left_img = left leg forward and *_right_img = right leg forward

        Each list is cyclically browsed with the variable 'self.steps'.

        :return: None
        """

        z_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_z.png').convert_alpha()
        z_left_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_zl.png').convert_alpha()
        z_right_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_zr.png').convert_alpha()
        self.z_images = [z_img, z_right_img, z_img, z_left_img]

        q_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_q.png').convert_alpha()
        q_left_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_ql.png').convert_alpha()
        q_right_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_qr.png').convert_alpha()
        self.q_images = [q_img, q_right_img, q_img, q_left_img]

        s_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_s.png').convert_alpha()
        s_left_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_sl.png').convert_alpha()
        s_right_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_sr.png').convert_alpha()
        self.s_images = [s_img, s_right_img, s_img, s_left_img]

        d_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_d.png').convert_alpha()
        d_left_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_dl.png').convert_alpha()
        d_right_img = pg.image.load(IMAGEDIR + 'player/' + self.name + '_dr.png').convert_alpha()
        self.d_images = [d_img, d_right_img, d_img, d_left_img]

    def get_image(self):
        """ Returns the image to display depending on where the player looks.

        'self.look_at' allows you to have the direction towards which the player is looking
        and 'self.steps' allows you to have the image to return in this direction.

        :return: the image to display, which is a Surface object
        """

        assert self.look_at in [(0, 1), (0, -1), (-1, 0), (1, 0)], "invalid coordinates"

        if self.look_at == (0, -1):
            return self.z_images[self.steps]
        elif self.look_at == (-1, 0):
            return self.q_images[self.steps]
        elif self.look_at == (1, 0):
            return self.d_images[self.steps]
        else:
            return self.s_images[self.steps]

    def move(self, dx=0, dy=0):
        """ Changes player x and y attributes.

        dx = 1/-1: the player moves one tile to the right/left
        dy = 1/-1: the player goes down/up one tile

        To accept the player to move, the destination tile shouldn't be out of bounds or an obstacle
        and the player can't move if he's interacting with a npc or an object.

        :param dx: x-axis offset
        :param dy: y-axis offset
        :return: None
        """

        assert -1 <= dx <= 1 and -1 <= dy <= 1, "dx and dy must be between -1 and 1"

        just_entered = False
        gate = self.on_gate()
        if gate is not None:  # The player is on a Gate object
            if dx == gate.dx and dy == gate.dy:  # The player has moved to enter the new map
                self.enter_gate(gate)
                just_entered = True

        if not self.game.paused and not just_entered:
            if not self.out_of_bounds(dx, dy) and not self.collide_with_obstacles(dx, dy) and not self.interacting:
                self.x += dx
                self.y += dy
                self.steps = (self.steps + 1) % 4

            if not self.interacting:  # It's rude not to look at somebody in the eye when he's talking to you.
                self.look_at = (dx, dy)  # Even if he doesn't move, he can rotate

    def out_of_bounds(self, dx=0, dy=0):
        """ Returns True if the player would be out of bounds.

        :param dx: x-axis offset
        :param dy: y-axis offset
        :return: True if the player would be out of bounds
        """

        map_x = self.game.map.width / TILESIZE
        map_y = self.game.map.height / TILESIZE
        if 0 <= self.x + dx < map_x and 0 <= self.y + dy < map_y:
            return False
        return True

    def collide_with_obstacles(self, dx=0, dy=0):
        """ Returns True if the player would collide with obstacles.

        :param dx: x-axis offset
        :param dy: y-axis offset
        :return: True if the player would collide with obstacles
        """

        for o in self.game.obstacles:
            if (o.x <= self.x + dx < (o.x + o.w)) and (o.y <= self.y + dy < (o.y + o.h)):
                return True
        return False

    def on_gate(self):
        """ If the player is on a gate, return this Gate object.

        :return: Gate object
        """

        for gate in self.game.gates:
            if gate.x == self.x and gate.y == self.y:
                return gate
        return None

    def enter_gate(self, gate):
        """ Loads a new map if the player enters a gate.

        Call the game method 'load_map'

        :param gate: the Gate object in which the player enters
        :return: None
        """

        self.game.load_map(gate.name, self.game.map.name)
        # gate.name = destination map, self.game.map.name = source map

        # set 'look_at' attribute depending on which side the gate is:
        self.look_at = (gate.dx, gate.dy)
        # to enter the new map the player must move like (dx, dy) so he keeps this position once in the new map

        # Reset 'steps' attribute when entering a new map:
        self.steps = 0

    def ready_to_interact(self):
        """ Returns True if the player is next to a npc or an object.

        :return: True if the player is next to a npc or an object
        """

        if self.interact_with_npc() is not None or self.interact_with_object() is not None:
            return True
        return False

    def interact_with_npc(self):
        """ Returns the NPC object next to which the player is, None otherwise.

        :return: the NPC object next to which the player is, None otherwise
        """

        for npc in self.game.characters:
            if (npc.x, npc.y) == (self.x + self.look_at[0], self.y + self.look_at[1]):
                return npc
        return None

    def interact_with_object(self):
        """ Returns the Object object next to which the player is, None otherwise.

        :return: the Object object next to which the player is, None otherwise
        """

        for obj in self.game.objects:  # unlike the characters, some objects are bigger than one tile
            if (obj.x <= self.x + self.look_at[0] < obj.x + obj.w) and (obj.y <= self.y + self.look_at[1] < obj.y + obj.h):
                return obj
        return None

    def update(self):
        """ Updates the player's rectangle x and y attributes.

        :return: None
        """

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        if self.steps >= 4:
            self.steps = 0


class Obstacle(pg.sprite.Sprite):
    """
        A class used to materialize the obstacles for the player,
        used in Player.collide_with_obstacles().

        Attributes
        ----------
        game: Game
            the 'Game' object from which this class was instantiated
        rect: Rect
            the rectangle created from the object dimensions
        x, y, w, h: int
            the coordinates on the map, the position in pixels divided by TILESIZE to have the tile index
            (x,y) coordinate is rectangle top-left corner
    """

    def __init__(self, game, x_px, y_px, w_px, h_px):
        self.groups = game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x_px, y_px, w_px, h_px)
        self.x = x_px/TILESIZE
        self.y = y_px/TILESIZE
        self.w = w_px/TILESIZE
        self.h = h_px/TILESIZE
        self.rect.x = x_px
        self.rect.y = y_px


class NPC(pg.sprite.Sprite):  # = Non-Player Character
    """
        A class used to represent a npc,
        npc = non-player character.

        Attributes
        ----------
        game: Game
            the 'Game' object from which this class was instantiated
        name: str
            the object name, used for quests
        type: str
            the object type, used to load corresponding images
        look_to: char
            default direction it looks to, is either 'z', 'q', 's' or 'd'
        interacting_with: bool
            variable indicating whether the player is interacting or not
        z_img, q_img, s_img, d_img: Image
            the image to display depending on where the player is looking to when interacting with the player
        default_image:
            the image to display when it is not interacting
        rect: Rect
            the rectangle created from the image
        x, y, w, h: int
            the coordinates on the map, the position in pixels divided by TILESIZE to have the tile index

        Methods
        -------
        get_image(self):
            returns the image to display depending on where the player is when interacting
    """

    def __init__(self, game, x_px, y_px, w_px, h_px, name, type, look_to):
        self.groups = game.all_sprites, game.obstacles, game.characters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.type = type
        self.look_to = look_to
        self.interacting_with = False

        self.z_img = pg.image.load(IMAGEDIR + 'npc/' + str(self.type) + '_z.png').convert_alpha()
        self.q_img = pg.image.load(IMAGEDIR + 'npc/' + str(self.type) + '_q.png').convert_alpha()
        self.s_img = pg.image.load(IMAGEDIR + 'npc/' + str(self.type) + '_s.png').convert_alpha()
        self.d_img = pg.image.load(IMAGEDIR + 'npc/' + str(self.type) + '_d.png').convert_alpha()

        if self.look_to == 'z':
            self.default_image = self.z_img
        elif self.look_to == 'q':
            self.default_image = self.q_img
        elif self.look_to == 'd':
            self.default_image = self.d_img
        else:
            self.default_image = self.s_img

        self.image_rect = self.default_image.get_rect()
        self.rect = pg.Rect(x_px, y_px, TILESIZE, TILESIZE)

        self.x = x_px/TILESIZE
        self.y = y_px/TILESIZE
        self.w = w_px/TILESIZE
        self.h = h_px/TILESIZE

    def __repr__(self):
        return "<%s sprite (%s) (in %d groups) - %s at (%d,%d)>" % (self.__class__.__name__, self.type, len(self.groups), self.name, self.x, self.y)

    def get_image(self):
        """ Returns the image to display depending on where the player is when interacting.

        Taking into account that the player must look at the npc to interact with it,
        we can use its 'look_at' attribute to return the correct image.

        :return: the image to display, which is a Surface object
        """

        if self.interacting_with:
            if self.game.player.look_at == (0, 1):
                return self.z_img
            elif self.game.player.look_at == (-1, 0):
                return self.d_img
            elif self.game.player.look_at == (1, 0):
                return self.q_img
            else:
                return self.s_img
        else:
            return self.default_image


class Object(pg.sprite.Sprite):
    """
        A class used to represent an object.

        Attributes
        ----------
        game: Game
            the 'Game' object from which this class was instantiated
        name: str
            the object name, used for quests
        type: str
            the object type, e.g. 'tree'
        image: Image
            the image to display depending on the type of the object
        rect: Rect
            the rectangle created from the image
        x, y, w, h: int
            the coordinates on the map, the position in pixels divided by TILESIZE to have the tile index

        Methods
        -------
        get_image(self):
            returns the image to display depending on where the player is when interacting
    """

    def __init__(self, game, x_px, y_px, w_px, h_px, name, type):
        self.groups = game.all_sprites, game.obstacles, game.objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.type = type

        self.image = pg.image.load(IMAGEDIR + 'objects/' + str(type) + '.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x_px/TILESIZE
        self.y = y_px/TILESIZE
        self.w = w_px/TILESIZE
        self.h = h_px/TILESIZE
        self.rect.x = x_px
        self.rect.y = y_px

    def __repr__(self):
        return "<%s sprite (%s) (in %d groups) - %s at (%d,%d)>" % (self.__class__.__name__, self.type, len(self.groups), self.name, self.x, self.y)

    def get_image(self):
        """ Returns the image to display depending on where the player is when interacting.

        Even if the method is very simple it is necessary so that the 'draw' method in Game class
        can use a 'get_image' method with all sprite in game.all_sprites group.

        :return: the image to display, which is a Surface object
        """

        return self.image


class Gate(pg.sprite.Sprite):
    """
        A class used to materialize the gates for the player,
        used in Player.enter_gate().

        Attributes
        ----------
        game: Game
            the 'Game' object from which this class was instantiated
        name: str
            the object name, the same name as the destination map
        rect: Rect
            the rectangle created from the object dimensions
        x, y: int
            the coordinates on the map, the position in pixels divided by TILESIZE to have the tile index
            (x,y) coordinate is rectangle top-left corner
        dx, dy: int
            the movement player must do to enter the new map
            e.g. for a gate placed against the upper edge of the map: dx=0, dy=-1 because the player must move as (0, -1)
    """

    def __init__(self, game, x_px, y_px, w_px, h_px, name, dx, dy):
        self.groups = game.gates
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.rect = pg.Rect(x_px, y_px, w_px, h_px)
        self.x = x_px/TILESIZE
        self.y = y_px/TILESIZE
        self.dx = dx
        self.dy = dy
