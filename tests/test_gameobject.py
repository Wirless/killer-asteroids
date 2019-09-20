import unittest
from unittest.mock import patch

import pygame

from killerasteroids import object, settings


class ScoreTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.test = object.Score()

    def test_score_start_at_zero(self):
        self.assertEqual(self.test.score, 0)
        self.assertEqual(self.test.text, f"SCORE: 0")

    def test_attribute_font_is_pygame_font(self):
        self.assertIsInstance(self.test.font, pygame.font.Font)

    def test_attribute_image_is_pygame_surface(self):
        self.assertIsInstance(self.test.image, pygame.Surface)

    def test_attribute_rect_is_pygame_rect(self):
        self.assertIsInstance(self.test.rect, pygame.Rect)

    def test_rect_position(self):
        self.assertEqual(self.test.rect.topleft, (10, 10))

    def test_update(self):
        self.test.score = 100
        self.test.update()
        self.assertEqual(self.test.text, f"SCORE: 100")

    def test_fire_score_when_zero(self):
        self.test.game_score("fire")
        self.assertEqual(self.test.score, 0)

    def test_fire_score_when_above_zero(self):
        self.test.score = 1
        self.test.game_score("fire")
        self.assertEqual(self.test.score, 0)


class LifeTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.test = object.Life()

    def test_life_at_start(self):
        self.assertEqual(self.test.life, 3)

    def test_life_text_at_start(self):
        self.assertEqual(self.test.text, "LIFE x 3")

    def test_attribute_font_is_pygame_font(self):
        self.assertIsInstance(self.test.font, pygame.font.Font)

    def test_attribute_image_is_pygame_surface(self):
        self.assertIsInstance(self.test.image, pygame.Surface)

    def test_attribute_rect_is_pygame_rect(self):
        self.assertIsInstance(self.test.rect, pygame.Rect)

    def test_rect_position(self):
        self.assertEqual(self.test.rect.topleft, (530, 10))

    def test_sound_effect_files(self):
        lose_file = self.test.lose_sfx.__dict__["file_exists"]
        gain_file = self.test.gain_sfx.__dict__["file_exists"]
        self.assertTrue(lose_file)
        self.assertTrue(gain_file)

    @patch("killerasteroids.object.Life.lose_life_sfx")
    def test_lose_life(self, mock_sfx):
        self.test.lose_life()
        self.assertEqual(self.test.life, 2)

    @patch("killerasteroids.object.Life.gain_life_sfx")
    def test_extra_life(self, mock_sfx):
        self.test.extra_life()
        self.assertEqual(self.test.life, 4)

    @patch("killerasteroids.object.Life.gain_life_sfx")
    def test_update(self, mock_sfx):
        self.test.extra_life()
        self.test.update()
        self.assertEqual(self.test.text, "LIFE x 4")
