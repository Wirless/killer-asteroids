#!/usr/bin/env python3.6

import unittest
from game import settings
from game.text import BannerText, MenuOptionText


class BannerTextTest(unittest.TestCase):

    def setUp(self):
        self.text = BannerText(25, "GAME OVER", [0, 50])

    def test_speed_setting(self):
        self.assertEqual(self.text.speed, [5, 0])

    def test_gameover_banner_update(self):
        self.text.update()
        self.assertEqual(self.text.rect[0], self.text.speed[0])


class MenuOptionTextTest(unittest.TestCase):

    def setUp(self):
        self.text = MenuOptionText(10, "Test", [1, 1], True)

    def test_if_color_is_set_to_active(self):
        """Make sure the color of the active option is correct."""
        # Update the option text so it get the active color.
        self.text.update()
        # Get the color at the position (1, 1) on the Surfaces.
        self.color = self.text.image.get_at_mapped((1, 1))
        # Convert RGB int to RGB.
        b, g, r = [(self.color >> (8*i)) & 255 for i in range(3)]
        # Check if it's the right color.
        self.assertEqual((r, g, b), settings.ACTIVE_OPTION)

    def test_get_state(self):
        self.assertTrue(self.text.get_state())

    def test_change_state(self):
        self.assertFalse(self.text.change_state())
