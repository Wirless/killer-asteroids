import os
import random
import pygame
from pygame import locals
from . import settings
from .sound import SoundEffect


class AnimatedObject(pygame.sprite.Sprite):
    """This class animates the game objects sprites."""

    def __init__(self, sprite, fps=10):
        super().__init__()

        self.file = sprite['file']
        self.size = sprite['size']
        self._images = self.load_sliced_sprites(self.size, self.file)
        self.image = pygame.Surface(self.size).convert()
        self.rect = self.image.get_rect()
        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1500 / fps
        self._last_update = 0
        self._frame = 0

    def animate(self, t):
        """This animates the game object.

        Note that this doesn't work if it's been more that self._delay
        time between calls to update(); we only update the image once
        then, but it really should be updated twice."""
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images):
                self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = t

    def load_sliced_sprites(self, size, file):
        """This loads the game objects sprite file and slices it into frames.

        The 'master' can be any height, but sprites frames width must be the
        same width. Master width must be len(frames)*frame.width."""

        w, h = size
        images = []
        master_image = pygame.image.load(file).convert_alpha()
        master_width, master_height = master_image.get_size()

        for i in range(int(master_width/w)):
            images.append(master_image.subsurface((i*w, 0, w, h)))
        return images


class Player(AnimatedObject):
    """This class is the playable game object.

    Takes two arguments:
    'sprite' - image file representing the objects appearance.
    'fps' - an optional argument that help determines the animation speed."""

    def __init__(self, sprite, fps=10):
        super().__init__(sprite, fps)
        self.rect.topleft = [0, 200]
        self.vertical = "STILL"
        self.horizontal = "STILL"
        self.speed = [5, 5]
        self.life = Life()
        self.score = Score()

    def update(self):
        """Update the players movments on the screen."""

        # Move spaceship vertical
        if self.vertical == "UP":
            if not self.rect[1] <= settings.LIMIT_UP:
                self.rect[1] -= self.speed[1]
        elif self.vertical == "DOWN":
            if not self.rect[1] >= settings.LIMIT_DOWN:
                self.rect[1] += self.speed[1]

        # Move spaceship horizontal
        if self.horizontal == "LEFT":
            if not self.rect[0] <= settings.LIMIT_LEFT:
                self.rect[0] -= self.speed[0]
        elif self.horizontal == "RIGHT":
            if not self.rect[0] >= settings.LIMIT_RIGHT:
                self.rect[0] += self.speed[0]

    def move(self, key):
        """Takes the user's input on how to steer the playable object."""

        if key == locals.K_UP:
            self.vertical = "UP"
        elif key == locals.K_DOWN:
            self.vertical = "DOWN"
        elif key == locals.K_LEFT:
            self.horizontal = "LEFT"
        elif key == locals.K_RIGHT:
            self.horizontal = "RIGHT"

    def stop_moving(self, key):
        """Stops the movement of the object if key is released."""

        if key == locals.K_UP or key == locals.K_DOWN:
            self.vertical = "STILL"
        if key == locals.K_LEFT or key == locals.K_RIGHT:
            self.horizontal = "STILL"

    def update_score(self, event):
        """Updates the players total score based on what happened ingame.

        The argument can be:
            'fire' - If the user fired the weapon.
            'damaged' - If the user got hit by an enemy object.
            'kill' - If the user destroyed an enemy object.
            'level up'- If the user cleared the current level."""
        self.score.game_score(event)

    def get_score(self):
        """Returns the current total score."""
        return self.score.score

    def get_extra_life(self):
        """Gives the player an extra life."""
        self.life.extra_life()

    def lose_life(self):
        """Remove one extra life from the player."""
        self.life.lose_life()

    def lives_left(self):
        """Returns the total extra lives the user currently has."""
        return self.life.life


class Laser(AnimatedObject):
    """This class is the laser weapon the player can fire.

    Takes three arguments:
    'sprite' - image file representing the objects appearance.
    'position' - the objects starting position.
    'fps' - an optional argument that help determines the animation speed."""

    def __init__(self, sprite, position, fps=10):
        super().__init__(sprite, fps)
        self.rect.center = position
        self.rect[1] += 5  # fix position of laser.
        self.sfx = SoundEffect(settings.LASER, 0.5)
        self.speed = [30, 0]

    def update(self):
        """Laser moves until it has reached the right side of the screen."""
        if self.rect[0] < settings.WIDTH:
            self.rect[0] += self.speed[0]

    def sound_effect(self):
        """Sound effect for the laser when fired."""
        self.sfx.play()


class Space(AnimatedObject):
    """This class creates a side-scrolling backgound.

    Takes three arguments:
    'sprite' - image file representing the objects appearance.
    'position' - the objects starting position.
    'fps' - an optional argument that help determines the animation speed."""

    def __init__(self, position, sprite, fps=10):
        super().__init__(sprite, fps)
        self.rect.topleft = position
        self.speed = [1, 0]

    def update(self):
        """Scroll the background to give an illusion of movement forward."""
        if self.rect[0] <= -settings.WIDTH:
            self.rect[0] = settings.WIDTH  # Reset the backgrounds position.
        else:
            self.rect[0] -= self.speed[0]


class Explosion(AnimatedObject):
    """This class creates an explosion.

    Takes three arguments:
    'sprite' - image file representing the objects appearance.
    'position' - the objects starting position.
    'fps' - an optional argument that help determines the animation speed."""

    def __init__(self, object, sprite, fps=10):
        super().__init__(sprite, fps)
        self.life = 15  # Object exists until zero is reached.
        self.rect.center = object.rect.center
        self.sfx = SoundEffect(settings.EXPLOSION, 0.4)

    def update(self):
        """Decreaces the objects life.

        When the life has reached zero the object shouldn't exist anymore."""
        self.life -= 1

    def sound_effect(self):
        """This is the objects sound effect."""
        self.sfx.play()


class PowerUpEffect(AnimatedObject):
    """This class creates a Power up object.

    Takes three arguments:
    'sprite' - image file representing the objects appearance.
    'position' - the objects starting position.
    'fps' - an optional argument that help determines the animation speed."""

    def __init__(self, object, sprite, fps=10):
        super().__init__(sprite, fps)
        self.life = 8  # Number that determines how long the object will exist.
        self.rect.center = object.rect.center
        self.sfx = SoundEffect(settings.POWER_UP, 0.4)

    def update(self):
        self.life -= 1

    def sound_effect(self):
        """This is the objects sound effect."""
        self.sfx.play()


class Asteroid(AnimatedObject):

    def __init__(self, sprite, position, speed, fps=10):
        super().__init__(sprite, fps)
        self.rect.topleft = position
        self.speed = speed

    def update(self):
        """Move asteroids."""
        if not self.rect[0] <= 0:
            self.rect[0] -= self.speed[0]
        else:
            self.rect.topleft = self.respawn()

    def respawn(self):
        x = random.randint(600, 1000)
        y = random.randint(20, 360)
        spawn_point = [x, y]
        return spawn_point


class PowerUp(AnimatedObject):

    def __init__(self, sprite, position, fps=10):
        super().__init__(sprite, fps)
        self.rect.topleft = position
        self.speed = [3, 0]

    def update(self):
        """Move power ups."""
        if self.rect[0] > -10:
            self.rect[0] -= self.speed[0]


class Score(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.text = f"SCORE: {self.score}"
        self.font = pygame.font.Font(settings.FONT, 15)
        self.image = self.font.render(self.text, 1, settings.TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = [10, 10]

    def update(self):
        self.text = f"SCORE: {self.score}"
        self.image = self.font.render(self.text, 1, settings.TEXT_COLOR)

    def game_score(self, event):
        if event == "fire":
            if self.score > 0:
                self.score -= 1
        elif event == "damaged":
            if self.score > 50:
                self.score -= 50
        elif event == "kill":
            self.score += 100
        elif event == "level up":
            self.score += 1000


class Life(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.life = 3
        self.text = f"LIFE x {self.life}"
        self.font = pygame.font.Font(settings.FONT, 15)
        self.image = self.font.render(self.text, 1, settings.TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = [530, 10]
        self.lose_sfx = SoundEffect(settings.BEEP, 0.7)
        self.gain_sfx = SoundEffect(settings.BEEP, 0.7)

    def update(self):
        self.text = f"LIFE x {self.life}"
        self.image = self.font.render(self.text, 1, settings.TEXT_COLOR)

    def gain_life_sfx(self):
        """Gain one extra life sound effect."""
        self.gain_sfx.play(1)
        self.gain_sfx.fadeout(5000)

    def lose_life_sfx(self):
        """Lose one life sound effect."""
        self.lose_sfx.play(10)
        self.lose_sfx.fadeout(2500)

    def extra_life(self):
        """Add one life."""
        self.gain_life_sfx()
        self.life += 1

    def lose_life(self):
        """Subtract one life."""
        self.lose_life_sfx()
        self.life -= 1
