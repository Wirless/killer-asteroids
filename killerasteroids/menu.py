import sys

import pygame
from pygame import locals

from . import settings
from .display import GameLoop, HelpSection, HighscoreSection
from .object import Space
from .sound import SoundEffect
from .text import GenericText, MenuOptionText


class Option:
    """Holds data about individual option in the menu."""

    def __init__(self, data):
        """Contains data about itself and pointers to adjacent options."""
        self.data = data
        self.next = None
        self.prev = None


class MenuOptions:
    """Class that builds and controls which option that is active."""

    def __init__(self, pos):
        """Initialize a doubly linked list for the menu options."""

        self._max = 0
        self._pos = pos
        self.head = None
        self.tail = None

        self.current = self.head

    @property
    def active(self):
        """Return active option."""

        if not self.current:
            self.current = self.head

        return self.current.data

    @property
    def all(self):
        """Return list with all options."""

        if not self.current:
            self.current = self.head

        name = self.current
        all = []

        for i in range(self._max):
            all.append(name.data)
            name = name.next

        return all

    @property
    def position(self):
        """Return option's position in menu."""
        return [self._pos[0], self._pos[1] + (20 * (self._max + 1))]

    @position.setter
    def position(self, pos):
        """Set menu's start position."""
        self._pos = pos

    # def add(self, data):
    def add(self, name, active=False, size=15):
        """Add new option to menu."""

        data = MenuOptionText(size, name, self.position, active)
        new_node = Option(data)
        self._max += 1

        if not self.head:
            self.head = new_node
            self.tail = new_node

            return True

        self.tail.next = new_node
        new_node.next = self.head
        new_node.prev = self.tail
        self.tail = new_node
        self.head.prev = self.tail

        return True

    def down(self):
        """Make next option active."""

        self.current.data.is_selected = False
        self.current = self.current.next
        self.current.data.is_selected = True

    def up(self):
        """Make previous option active."""

        self.current.data.is_selected = False
        self.current = self.current.prev
        self.current.data.is_selected = True


class MenuScreen:
    """Main menu screen."""

    def __init__(self):

        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen_size = (settings.WIDTH, settings.HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(settings.CAPTION)
        pygame.mouse.set_visible(0)

        # Sprites.
        self.title = GenericText(25, settings.CAPTION, [150, 50])
        self.space_sprites = [
            Space([0, 0], settings.SPACE_SPRITE),
            Space([640, 0], settings.SPACE_SPRITE),
        ]

        self.option = MenuOptions([250, 150])
        self.option.add("START GAME", active=True)
        self.option.add("HIGHSCORE")
        self.option.add("HELP")
        self.option.add("QUIT")

        # Groups.
        self.space_group = pygame.sprite.RenderPlain(self.space_sprites)
        self.menu_group = pygame.sprite.RenderPlain(self.title, self.option.all)

        # Sound effects.
        self.choice_sfx = SoundEffect(settings.MENU_BEEP, 0.5)
        self.startgame_sfx = SoundEffect(settings.START_GAME, 1.0)

    def update(self, key):
        """Update and activate option in menu."""

        if key == locals.K_DOWN:
            self.choice_sfx.play()
            self.option.down()

        elif key == locals.K_UP:
            self.choice_sfx.play()
            self.option.up()

        elif key == locals.K_RETURN:
            active = self.option.active.text

            if active == "START GAME":
                self.startgame_sfx.play()
                GameLoop().main()

            elif active == "HIGHSCORE":
                HighscoreSection(self.screen, self.space_group).main()

            elif active == "HELP":
                HelpSection(self.screen, self.space_group).main()

            elif active == "QUIT":
                sys.exit()

    def game_menu(self):
        """Menu screen loop."""

        while True:
            pygame.time.Clock().tick(settings.FPS)

            # Handle user input.
            for event in pygame.event.get():
                if event.type == locals.KEYDOWN:
                    menu_exit = (
                        event.type == locals.QUIT
                        or event.type == locals.KEYDOWN
                        and event.key == locals.K_ESCAPE
                    )
                    menu_event = (
                        event.key == locals.K_UP
                        or event.key == locals.K_DOWN
                        or event.key == locals.K_RETURN
                    )

                    if menu_exit:
                        sys.exit()
                    elif menu_event:
                        self.update(event.key)

            # Animate space.
            for space in self.space_group.sprites():
                space.animate(pygame.time.get_ticks())

            # Update sprites.
            self.space_group.update()
            self.menu_group.update()

            # Draw sprites.
            self.screen.fill(settings.BG_COLOR)
            self.space_group.draw(self.screen)
            self.menu_group.draw(self.screen)

            pygame.display.update()
