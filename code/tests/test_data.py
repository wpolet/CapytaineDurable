import unittest
from data import quests, interaction_texts, goals


class TestData(unittest.TestCase):

    def test_quests(self):
        quests_name = []
        for q in quests:
            quests_name.append(q["name"])
            self.assertTrue(len(q["dialogue"]) >= 3)
            self.assertIn(q["npc1_name"], interaction_texts)
            self.assertIn(q["npc2_name"], interaction_texts)

            if q["quest_type"] == 2:
                self.assertTrue(len(q["dialogue"]) == 4)
                self.assertIsNotNone(q["obj_type"])
                self.assertIsNotNone(q["obj_nbr"])

        try:
            self.assertTrue(len(quests_name) == len(set(quests_name)))
        except AssertionError:
            for q in quests:
                if quests_name.count(q["name"]) > 1:
                    print("Error: At least 2 quests have the name " + q["name"])
                    break
            raise AssertionError

    def test_goals(self):
        for g in goals:
            self.assertIsNotNone(g["title"])
            self.assertIsNotNone(g["expl"])
            self.assertIsNotNone(g["advice"])
            self.assertIsNotNone(g["facts"])
            self.assertIsNotNone(g["color"])


if __name__ == '__main__':
    unittest.main()
