import sys

import pygame
from pygame import locals

from . import settings
from .display import GameLoop, HelpSection, HighscoreSection
from .object import Space
from .sound import SoundEffect
from .text import GenericText, MenuOptionText


class MainMenu:
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
        self.options = [
            MenuOptionText(15, "START GAME", [250, 150], True),
            MenuOptionText(15, "HIGHSCORE", [250, 170], False),
            MenuOptionText(15, "HELP", [250, 190], False),
            MenuOptionText(15, "QUIT", [250, 210], False),
        ]
        # Groups.
        self.space_group = pygame.sprite.RenderPlain(self.space_sprites)
        self.menu_group = pygame.sprite.RenderPlain(self.title, self.options)
        # Sound effects.
        self.choice_sfx = SoundEffect(settings.MENU_BEEP, 0.5)
        self.startgame_sfx = SoundEffect(settings.START_GAME, 1.0)

    def update_selected_option(self, key):

        current = None
        for option in self.options:
            if option.get_state():
                current = option.text

        if key == locals.K_DOWN:
            self.choice_sfx.play()
            if current == "START GAME":
                self.options[0].change_state()
                self.options[1].change_state()
            elif current == "HIGHSCORE":
                self.options[1].change_state()
                self.options[2].change_state()
            elif current == "HELP":
                self.options[2].change_state()
                self.options[3].change_state()
            elif current == "QUIT":
                self.options[3].change_state()
                self.options[0].change_state()

        elif key == locals.K_UP:
            self.choice_sfx.play()
            if current == "START GAME":
                self.options[0].change_state()
                self.options[3].change_state()
            elif current == "HIGHSCORE":
                self.options[1].change_state()
                self.options[0].change_state()
            elif current == "HELP":
                self.options[2].change_state()
                self.options[1].change_state()
            elif current == "QUIT":
                self.options[3].change_state()
                self.options[2].change_state()

        elif key == locals.K_RETURN:
            if current == "START GAME":
                self.startgame_sfx.play()
                GameLoop().main()
            elif current == "HIGHSCORE":
                HighscoreSection(self.screen, self.space_group).main()
            elif current == "HELP":
                HelpSection(self.screen, self.space_group).main()
            elif current == "QUIT":
                sys.exit()

    def main(self):

        while True:
            pygame.time.Clock().tick(settings.FPS)

            for event in pygame.event.get():
                if (
                    event.type == locals.QUIT
                    or event.type == locals.KEYDOWN
                    and event.key == locals.K_ESCAPE
                ):
                    sys.exit()
                if event.type == locals.KEYDOWN:
                    if (
                        event.key == locals.K_UP
                        or event.key == locals.K_DOWN
                        or locals.K_RETURN
                    ):
                        self.update_selected_option(event.key)

            # Animate space.
            for space in self.space_group.sprites():
                space.animate(pygame.time.get_ticks())

            # Update the screen
            self.space_group.update()
            self.menu_group.update()

            # Draw
            self.screen.fill(settings.BG_COLOR)
            self.space_group.draw(self.screen)
            self.menu_group.draw(self.screen)

            pygame.display.update()
