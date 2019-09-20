import random

import pygame

from . import settings
from .object import Asteroid, PowerUp
from .sound import SoundEffect


class LevelDesign(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.current_level = 1
        self.level_design = self.generate_level()
        self.font = pygame.font.Font(settings.FONT, 15)
        self.text = f"LEVEL: {self.current_level}"
        self.image = self.font.render(self.text, 1, settings.TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = [270, 10]
        self.sfx = SoundEffect(settings.LEVEL_UP, 0.5)

    def update(self):
        self.text = f"LEVEL: {self.current_level}"
        self.image = self.font.render(self.text, 1, settings.TEXT_COLOR)

    def get_level(self):
        return self.level_design

    def next_level(self):
        self.sfx.play()
        self.current_level += 1
        self.level_design = self.generate_level()

        return self.level_design

    def _get_enemies(self):
        """Generates enemies, which is tripled each level up."""
        num = self.current_level * 3  # Total number of objects on this level.
        enemies = []
        for enemy in range(num):
            x = random.randint(600, 2000)
            y = random.randint(settings.LIMIT_UP, settings.LIMIT_DOWN)
            pos = [x, y]
            speed = [random.randint(3, 6), 0]
            enemies.append(Asteroid(settings.ASTEROID_SPRITE, pos, speed))

        return enemies

    def _get_powerups(self):
        """Generates one or zero powerup for the level."""
        num = random.randint(0, 1)
        powerups = []
        for powerup in range(num):
            x = random.randint(600, 2000)
            y = random.randint(settings.LIMIT_UP, settings.LIMIT_DOWN)
            pos = [x, y]
            powerups.append(PowerUp(settings.POWER_UP_SPRITE, pos))

        return powerups

    def generate_level(self):
        """Returns a tuple with all objects for the level."""
        enemies = self._get_enemies()
        powerups = self._get_powerups()
        objs = (enemies, powerups)

        return objs
