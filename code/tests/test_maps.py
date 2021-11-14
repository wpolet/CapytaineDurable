import pygame as pg
import unittest
import pytmx

from data import interaction_texts
from settings import GAME_STARTUP_PARAMS


pg.init()
pg.display.set_mode((100, 100))

maps_name = ["map0", "map1", "map1_2", "map2", "map2_2", "map2_3", "map3", "map4", "map4_2", "mapB", "mapC", "mapC_2", "mapC_3", "mapD", "mapD_2", "mapD_3"]


class TestMaps(unittest.TestCase):

    def test_load_map(self):
        for map_name in maps_name:
            map_data = pytmx.load_pygame('../maps/' + map_name + '.tmx', pixelalpha=True)

            for obj in map_data.objects:
                if obj.type == "gate":
                    self.assertIsNotNone(obj.name)
                    self.assertIsNotNone(obj.dx)
                    self.assertIsNotNone(obj.dy)
                elif obj.type[0:3] == "npc":
                    self.assertIn(obj.name, interaction_texts)
                    self.assertIsNotNone(obj.name)
                    self.assertIsNotNone(obj.type)
                    self.assertIsNotNone(obj.look_to)
                elif obj.type[0:-1] in ["tree", "dirt", "rock", "trash"]:
                    self.assertIsNotNone(obj.name)
                    self.assertIsNotNone(obj.type)


if __name__ == '__main__':
    unittest.main()