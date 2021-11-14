"""
    This module manages the creation of the displayed map
    and the placement of the different objects on this map
    then shifts the map and the objects according to the player's movements.

    Class
    -----
    TiledMap:
        a class used to create the tiled map
    Camera:
        a class used to select the section of the map to display on the screen
        and to move each object with the same offset
"""

import pygame as pg
import pytmx

from settings import WIDTH, HEIGHT, TILESIZE


class TiledMap:
    """
        A class used to create the tiled map,
        maps are created with Tiled editor and stored in 'maps' folder.

        Attributes
        ----------
        tmxdata: pytmx data
            all data from the '.tmx' file
        width: int (pixels)
            the map width
        height: int (pixels)
            the map heigth
        name: str
            the map name
        image: Image
            the image to display, created from the map
        rect: Rect
            the rectangle created from the image

        Methods
        -------
        make_map(self):
            creates the map image
    """

    def __init__(self, game, map_name):
        map_version = game.script.maps_version[map_name] if map_name in game.script.maps_version else ''
        self.tmxdata = pytmx.load_pygame('maps/' + map_name + map_version + '.tmx', pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        self.name = map_name

        self.image = self.make_map()
        self.rect = self.image.get_rect()

    def make_map(self):
        """ Creates the map image.

        The image is a Surface object with the dimensions of the map
        and with all tiles and objects on it.

        :return: the map image, which is a Surface object
        """

        temp_surface = pg.Surface((self.width, self.height))

        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        temp_surface.blit(tile, (x * TILESIZE, y * TILESIZE))

        return temp_surface


class Camera:
    """
        A class used to select the section of the map to display on the screen
        and to move each object with the same offset.

        When the dimensions of the map are larger than those of the screen,
        it is necessary to create an offset for the player to walk on the map
        while remaining in the center of the screen
        (except when he reaches the limits of the map).

        Attributes
        ----------
        camera: Rect
            a rectangle with the dimensions of the map used to manage the screen offset
        width: int (pixels)
            the map width
        height: int (pixels)
            the map height

        Methods
        -------
        apply(self, entity):
            function to apply to each object to have the same offset
        update(self, target):
            calculates the offset and shift the camera accordingly
    """

    def __init__(self, map_width, map_height):
        self.camera = pg.Rect(0, 0, map_width, map_height)
        self.width = map_width
        self.height = map_height

    def apply(self, entity):
        """ Function to apply to each object to have the same offset.

        To keep the player in the center of the screen,
        we shift the map and all the objects in the opposite direction of its movement.
        Which gives the impression that the player is moving.

        :param entity: is either a Rect object or an object with a 'rect' attribute
        :return: Rect object used to know the x and y object position
        """

        if self.width > WIDTH:
            x = self.camera.x
        else:
            x = (WIDTH - self.width) / 2

        if self.height > HEIGHT:
            y = self.camera.y
        else:
            y = (HEIGHT - self.height) / 2

        if isinstance(entity, pg.Rect):
            return entity.move(x,y)
        else:
            assert entity.rect is not None, "the object must have a rect attribute"
            return entity.rect.move(x,y)

    def update(self, target):
        """ Calculates the offset and shift the camera accordingly.

        Function call in the 'update' method of the Game class
        where the 'target' parameter is the game Player object.

        The player is always in the center of the screen
        except when the camera reaches a map limit and the player
        continues to advance in this direction.

        :param target: an object with a Rect object attribute, typically the player.
        :return: None
        """

        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # Limit scrolling to map size:
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)
        # The map will be drawn with an offset of x and y
