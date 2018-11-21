import pygame
from . import settings


class RenderText(pygame.sprite.Sprite):
    """Creates an text object with specified content and font size.

    This is the parent class that all the different text objects
    in the game should inherit from."""

    def __init__(self, size, text):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(settings.FONT, size)
        self.image = self._render_text(self.text, settings.TEXT_COLOR)
        self.rect = self.image.get_rect()

    def _render_text(self, text, color):
        return self.font.render(text, True, color)


class GenericText(RenderText):
    """This class is for creating generic text objects.

    Text objects that doesn't need to do anything special
    should use this class. Arguments needed is the font size,
    a text string and a list with x and y coordinates."""

    def __init__(self, size, text, position):
        super().__init__(size, text)
        self.rect.topleft = position


class BannerText(GenericText):
    """This class makes the text scrolling around on the screen."""

    def __init__(self, size, text, position):
        super().__init__(size, text, position)
        self.speed = [5, 0]

    def update(self):
        """Indefinetly scroll text from left to right side of screen."""

        if not self.rect[0] >= settings.WIDTH + 300:
            self.rect[0] += self.speed[0]
        else:
            self.rect[0] = -200


class MenuOptionText(GenericText):
    """This class is for different options on a menu."""

    def __init__(self, size, text, position, selected):
        super().__init__(size, text, position)
        self.is_selected = selected

    def update(self):
        """Change the color of the options to indicate which on is active."""
        if self.get_state():
            self.image = self._render_text(self.text, settings.ACTIVE_OPTION)
        else:
            self.image = self._render_text(self.text, settings.TEXT_COLOR)

    def get_state(self):
        """Tells if the option is selected or not."""
        return self.is_selected

    def change_state(self):
        """This changes the state of the option."""
        if self.get_state():
            self.is_selected = False
        else:
            self.is_selected = True
