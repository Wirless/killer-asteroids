import unittest

import pygame

from killerasteroids import settings, text


class TestRenderText(unittest.TestCase):
    def setUp(self):
        self.test = text.RenderText(15, "test")

    def test_attribute_text_is_string(self):
        self.assertIsInstance(self.test.text, str)

    def test_attribute_font_is_pygame_font(self):
        self.assertIsInstance(self.test.font, pygame.font.Font)

    def test_attribute_image_is_pygame_surface(self):
        self.assertIsInstance(self.test.image, pygame.Surface)

    def test_attribute_rect_is_pygame_rect(self):
        self.assertIsInstance(self.test.rect, pygame.Rect)

    def test_render_text_return_surface(self):
        got = self.test._render_text("test", (0, 0, 0))
        self.assertIsInstance(got, pygame.Surface)


class TestGenericText(unittest.TestCase):
    def setUp(self):
        self.position = (1, 1)
        self.test = text.GenericText(15, "test", self.position)

    def test_rect_position(self):
        self.assertEqual(self.test.rect.topleft, self.position)


class TestBannerText(unittest.TestCase):
    def setUp(self):
        self.test = text.BannerText(25, "GAME OVER", [0, 50])

    def test_speed_setting(self):
        self.assertEqual(self.test.speed, [5, 0])

    def test_gameover_banner_update(self):
        self.test.update()
        self.assertEqual(self.test.rect[0], self.test.speed[0])


class TestMenuOptionText(unittest.TestCase):
    def setUp(self):
        self.test = text.MenuOptionText(10, "Test", [1, 1], True)

    def test_if_color_is_set_to_active(self):
        # Update the option text so it get the active color.
        self.test.update()
        # Get the color at the position (1, 1) on the Surfaces.
        self.color = self.test.image.get_at_mapped((1, 1))
        # Convert RGB int to RGB.
        b, g, r = [(self.color >> (8 * i)) & 255 for i in range(3)]
        # Check if it's the right color.
        self.assertEqual((r, g, b), settings.ACTIVE_OPTION)

    def test_get_state(self):
        self.assertTrue(self.test.get_state())

    def test_change_state(self):
        self.assertFalse(self.test.change_state())
