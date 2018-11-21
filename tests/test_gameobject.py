#!/usr/bin/env python3.6

import unittest
import pygame
from game import settings
from game import object


class PowerUpTest(unittest.TestCase):

    def setUp(self):
        pass


class ScoreTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.obj = object.Score()

    def test_update(self):
        """Test so the score text is updating correctly."""
        self.obj.score = 100
        self.obj.update()
        self.assertEqual(self.obj.text, f"SCORE: 100")

    def test_fire_score_when_zero(self):
        self.obj.game_score("fire")
        self.assertEqual(self.obj.score, 0)

    def test_fire_score_when_above_zero(self):
        self.obj.score = 1
        self.obj.game_score("fire")
        self.assertEqual(self.obj.score, 0)


class LifeTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.obj = object.Life()

    def test_life_at_start(self):
        """Test if there are 3 extra lives at the start of the game."""
        self.assertEqual(self.obj.life, 3)

    def test_life_text_at_start(self):
        """Test the display text of the number of lives."""
        self.assertEqual(self.obj.text, "LIFE x 3")

    def test_lose_life(self):
        """Test if the starting life decreaces by one if player loses life."""
        self.obj.lose_life()
        self.assertEqual(self.obj.life, 2)

    def test_extra_life(self):
        """Starting life increaces by one if player gain extra life."""
        self.obj.extra_life()
        self.assertEqual(self.obj.life, 4)

    def test_update(self):
        """Testing that the extra life indicator is updating correctly."""
        self.obj.extra_life()
        self.obj.update()
        self.assertEqual(self.obj.text, "LIFE x 4")


if __name__ == "__main__":
    unittest.main()
