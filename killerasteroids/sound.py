import os.path

import pygame


class SoundEffect:
    """This class handles the sound effects in the game."""

    def __init__(self, file, volume):
        self.file_exists = os.path.isfile(file)  # Check if file exists.
        if self.file_exists:
            self.sfx = self.load_sound(file)
            self.sfx.set_volume(volume)
        else:
            print(f"ERROR: {self.file} is missing.")

    def load_sound(self, file):
        """This will load the sound effect from the file."""

        class NoneSound:
            def play(self):
                pass

        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        try:
            sound = pygame.mixer.Sound(file)
        except pygame.error:
            print("Cannot load sound:", file)
            raise SystemExit
        return sound

    def play(self, loop=0):
        """This will play the sound effect."""
        if self.file_exists:
            self.sfx.play(loop)

    def fadeout(self, time):
        """Fade out the volume over for some milliseconds."""
        if self.file_exists:
            self.sfx.fadeout(time)


class BackgroundMusic:
    """This class handles the background music in the game."""

    def __init__(self, file, volume):
        self.music = pygame.mixer.music
        self.file = file
        self.file_exists = os.path.isfile(self.file)  # Check if file exists.
        if self.file_exists:
            self.load(self.file)
            self.set_volume(volume)
        else:
            print(f"ERROR: {self.file} is missing.")

    def load(self, file):
        """This will load the music file."""
        if self.file_exists:
            self.music.load(file)

    def set_volume(self, volume):
        """This will set the volume of the music."""
        if self.file_exists:
            self.music.set_volume(volume)

    def play(self):
        """This will start the music and repeat it indefinitely."""
        if self.file_exists:
            self.music.play(-1)

    def stop(self):
        """This will stop the music."""
        if self.file_exists:
            self.music.stop()
