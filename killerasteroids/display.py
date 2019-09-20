import os
import sqlite3
import sys
import time

import pygame
from pygame import locals

from . import settings
from .level import LevelDesign
from .object import Explosion, Laser, Player, PowerUpEffect, Space
from .sound import BackgroundMusic, SoundEffect
from .text import BannerText, GenericText, MenuOptionText


class GameLoop:
    """This class contains the actuall game."""

    def __init__(self):
        """Initialize the necessary settings to run the game."""

        self.frame_rate = pygame.time.Clock()
        self.screen_size = (settings.WIDTH, settings.HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(settings.CAPTION)
        pygame.mouse.set_visible(0)
        # Changes to false after game is over.
        self.playing = True
        # Background music
        self.bg_music = BackgroundMusic(settings.BG_MUSIC, 0.5)
        # Sprites
        self.player_sprite = Player(settings.PLAYER_SPRITE)
        self.space_sprites = [
            Space([0, 0], settings.SPACE_SPRITE),
            Space([640, 0], settings.SPACE_SPRITE),
        ]
        # Generate level.
        self.level = LevelDesign()
        self.enemies, self.powerups = self.level.get_level()
        # Groups
        self.laser_group = pygame.sprite.RenderPlain()
        self.effect_group = pygame.sprite.RenderPlain()
        self.asteroid_group = pygame.sprite.RenderPlain(self.enemies)
        self.powerup_group = pygame.sprite.RenderPlain(self.powerups)
        self.space_group = pygame.sprite.RenderPlain(self.space_sprites)
        self.player_group = pygame.sprite.RenderPlain(self.player_sprite)
        self.player_stats_group = pygame.sprite.RenderPlain(
            self.player_sprite.life, self.player_sprite.score, self.level
        )

    def animate_groups(self):
        """Animate the sprites in the groups in this method."""
        for space in self.space_group.sprites():
            space.animate(pygame.time.get_ticks())
        for laser in self.laser_group.sprites():
            laser.animate(pygame.time.get_ticks())
        for spaceship in self.player_group.sprites():
            spaceship.animate(pygame.time.get_ticks())
        for asteroid in self.asteroid_group.sprites():
            asteroid.animate(pygame.time.get_ticks())
        for powerup in self.powerup_group.sprites():
            powerup.animate(pygame.time.get_ticks())
        for explosion in self.effect_group.sprites():
            explosion.animate(pygame.time.get_ticks())

    def update_groups(self):
        """Update the sprites in the groups in this method."""
        self.space_group.update()
        self.laser_group.update()
        self.player_group.update()
        self.asteroid_group.update()
        self.powerup_group.update()
        self.effect_group.update()
        self.player_stats_group.update()

    def draw_groups(self):
        """Draw the sprites to the screen in the groups in this method."""
        self.space_group.draw(self.screen)
        self.laser_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.asteroid_group.draw(self.screen)
        self.powerup_group.draw(self.screen)
        self.effect_group.draw(self.screen)
        self.player_stats_group.draw(self.screen)

    def clean_groups(self):
        """Delete unnecessary sprites in the groups in this method."""
        # Removes lasers that has reached the right side of the screen.
        for laser in self.laser_group.sprites():
            if laser.rect[0] > settings.WIDTH:
                self.laser_group.remove(laser)
        # Remove powerups that has reached the left edge of the screen.
        for powerup in self.powerup_group.sprites():
            if powerup.rect[0] < 0:
                self.powerup_group.remove(powerup)
        # Removes explosions that has looped through the animation one time.
        for explosion in self.effect_group.sprites():
            if not explosion.life:
                self.effect_group.remove(explosion)

    def reset_game(self):
        """Things to do after done playing the game."""

        total_score = self.player_sprite.get_score()
        GameOver(self.screen, self.space_group).run(total_score)
        # Stop the music from playing before returning to the main menu.
        self.bg_music.stop()
        # Stop the game loop after the 'gameover' screen.
        self.playing = False

    def player_gets_powerup(self, player, powerup):
        """Does things if the player picks up a power up object."""

        hit = pygame.sprite.groupcollide(powerup, player, True, False)
        if hit:
            self.effect_group.add(
                PowerUpEffect(
                    self.player_sprite,
                    settings.POWER_UP_EFFECT_SPRITE,
                    pygame.time.get_ticks(),
                )
            )

            for powerup in self.effect_group.sprites():
                powerup.sound_effect()
            self.player_sprite.get_extra_life()

    def asteroid_hits_player(self, asteroid, player):
        """Does things if an asteroid hits the player."""

        hit = pygame.sprite.groupcollide(asteroid, player, True, False)

        if hit:
            self.player_sprite.update_score("damaged")
            self.player_sprite.lose_life()
            self.effect_group.add(
                Explosion(
                    self.player_sprite,
                    settings.EXPLOSION_SPRITE,
                    pygame.time.get_ticks(),
                )
            )

            for explosion in self.effect_group.sprites():
                explosion.sound_effect()

            if self.player_sprite.lives_left() == 0:  # Game over.
                self.reset_game()

    def laser_hits_asteroid(self, laser, asteroid):
        """Does things if the laser hits the asteroids."""

        hit = None
        active_laser = len(self.laser_group)

        if active_laser:
            hit = pygame.sprite.groupcollide(laser, asteroid, True, True)

        if hit:
            # Create explosion object and explosion sound.
            self.player_sprite.update_score("kill")
            # The laser obj is not important therefore it's an underscore.
            for _, asteroid_position in hit.items():
                self.effect_group.add(
                    Explosion(
                        asteroid_position[0],  # The list has only one item.
                        settings.EXPLOSION_SPRITE,
                        pygame.time.get_ticks(),
                    )
                )

            for explosion in self.effect_group.sprites():
                explosion.sound_effect()

    def is_asteroids_destroyed(self):
        """Go to the next level if all asteroids are destroyed."""

        if not len(self.asteroid_group):
            self.player_sprite.update_score("level up")
            self.enemies, self.powerups = self.level.next_level()
            self.asteroid_group.add(self.enemies)
            self.powerup_group.add(self.powerups)

    def main(self):
        """The games main method that cointains the game loop."""
        # Start playing the backgound music.
        self.bg_music.play()

        while self.playing:

            # Set the maximum frame rate.
            self.frame_rate.tick(settings.FPS)

            # Handle all user events.
            for event in pygame.event.get():
                # Exit anytime by pressing escape or the window's close button.
                if (
                    event.type == locals.QUIT
                    or event.type == locals.KEYDOWN
                    and event.key == locals.K_ESCAPE
                ):
                    sys.exit()
                # Makes the spaceship move smoother.
                if event.type == locals.KEYUP:
                    # The spaceship stops moving if the keys are released.
                    if (
                        event.key == locals.K_UP
                        or event.key == locals.K_DOWN
                        or event.key == locals.K_LEFT
                        or event.key == locals.K_RIGHT
                    ):
                        for spaceship in self.player_group.sprites():
                            spaceship.stop_moving(event.key)
                # Makes the spaceship move.
                if event.type == locals.KEYDOWN:
                    # Control the spaceship.
                    if (
                        event.key == locals.K_UP
                        or event.key == locals.K_DOWN
                        or event.key == locals.K_LEFT
                        or event.key == locals.K_RIGHT
                    ):
                        for spaceship in self.player_group.sprites():
                            spaceship.move(event.key)
                    # Fire weapon.
                    if event.key == locals.K_SPACE:
                        # lose one point everytime lasergun is fired
                        self.player_sprite.update_score("fire")
                        self.laser_group.add(
                            Laser(
                                settings.LASER_SPRITE,
                                self.player_sprite.rect.center,
                            )
                        )
                        for laser in self.laser_group.sprites():
                            laser.sound_effect()
                    # Pause game.
                    if event.key == locals.K_p:
                        self.bg_music.stop()  # Stop music when paused.
                        value = PauseMenu(
                            self.screen,
                            self.space_group,
                            self.laser_group,
                            self.player_group,
                            self.asteroid_group,
                            self.powerup_group,
                            self.effect_group,
                        ).main()
                        self.bg_music.play()  # Start music when game resumes.
                        if value == "RESTART GAME":
                            print(value)

            # Collision detection.
            self.laser_hits_asteroid(self.laser_group, self.asteroid_group)
            self.asteroid_hits_player(self.asteroid_group, self.player_group)
            self.player_gets_powerup(self.player_group, self.powerup_group)
            self.is_asteroids_destroyed()

            if self.playing:
                # Animate the sprites in the groups.
                self.animate_groups()
                # Update the sprites in the groups.
                self.update_groups()
                # Draw over everything to clean up previously drawn sprites.
                self.screen.fill(settings.BG_COLOR)
                # Draw the sprites in the groups to the screen.
                self.draw_groups()
                # Clean up sprites no longer useful.
                self.clean_groups()

            # Make everything visible on the screen for the user.
            pygame.display.update()


class PauseMenu:
    def __init__(self, screen, *args):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.groups = [group.sprites() for group in args]
        self.banner = GenericText(35, "PAUSE", [250, 130])

        # Pause menu options.
        self.options = [
            MenuOptionText(15, "RESUME", [283, 180], True),
            MenuOptionText(15, "QUIT", [295, 200], False),
        ]

        self.text_group = pygame.sprite.RenderPlain(self.banner)
        self.menu_group = pygame.sprite.RenderPlain(self.options)
        self.group_group = [pygame.sprite.RenderPlain(g) for g in self.groups]

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

            if current == "RESUME":
                self.options[0].change_state()
                self.options[1].change_state()
            elif current == "QUIT":
                self.options[0].change_state()
                self.options[1].change_state()

        elif key == locals.K_UP:

            self.choice_sfx.play()

            if current == "RESUME":
                self.options[0].change_state()
                self.options[1].change_state()
            elif current == "QUIT":
                self.options[0].change_state()
                self.options[1].change_state()

        elif key == locals.K_RETURN:
            if current == "RESUME":
                return "RESUME GAME"
            elif current == "QUIT":
                sys.exit()

    def dim_screen(self):
        """Create an transparent surface to dim the screen."""
        # Creates a surface that covers the entire screen.
        dimmed = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        # Set the alpha level to make it transparent and fill it with a color.
        dimmed.set_alpha(100)
        dimmed.fill(settings.BG_COLOR)
        # Draw it to the screen.
        self.screen.blit(dimmed, (0, 0))

    def main(self):

        while True:
            self.clock.tick(settings.FPS)
            for event in pygame.event.get():
                if (
                    event.type == locals.QUIT
                    or event.type == locals.KEYDOWN
                    and event.key == locals.K_ESCAPE
                ):
                    sys.exit()
                if event.type == locals.KEYDOWN:
                    if event.key == locals.K_p:
                        return
                if event.type == locals.KEYDOWN:
                    if (
                        event.key == locals.K_UP
                        or event.key == locals.K_DOWN
                        or locals.K_RETURN
                    ):
                        choice = self.update_selected_option(event.key)
                        if choice == "RESUME GAME":
                            return

            # Animate groups.
            for group in self.group_group:
                for sprite in group.sprites():
                    sprite.animate(pygame.time.get_ticks())

            # Update the screen
            self.text_group.update()
            self.menu_group.update()

            # draw space
            self.screen.fill(settings.BG_COLOR)
            for group in self.group_group:
                group.draw(self.screen)
            self.dim_screen()
            self.text_group.draw(self.screen)
            self.menu_group.draw(self.screen)

            pygame.display.update()


class HighscoreSection:
    def __init__(self, screen, group):

        self.screen = screen
        self.space = group.sprites()  # The scrolling background.
        self.space_group = pygame.sprite.RenderPlain(self.space)
        self.db = GameDatabase()
        self.db.create_table()
        self.title = GenericText(20, "HIGHSCORE:", [250, 100])
        self.text = self.db.get_highscore_list()
        self.text_group = pygame.sprite.RenderPlain(self.title, self.text)

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
                    if event.key == locals.K_BACKSPACE:
                        return

            # Animate space.
            for space in self.space_group.sprites():
                space.animate(pygame.time.get_ticks())

            # Update the screen.
            self.space_group.update()
            self.text_group.update()

            # Draw.
            self.screen.fill(settings.BG_COLOR)
            self.space_group.draw(self.screen)
            self.text_group.draw(self.screen)

            pygame.display.update()


class GameDatabase:
    def __init__(self):
        self._check_dir(settings.DATABASE)
        self.db_conn = sqlite3.connect(settings.DATABASE)
        self.db_curs = self.db_conn.cursor()
        self.create_table()

    def _check_dir(self, database):
        """Create directory if not exists"""
        if not os.path.exists(os.path.dirname(database)):
            os.mkdir(os.path.dirname(database))

    def create_table(self):
        """Creates a new table if it doesn't exist."""
        query = (
            "CREATE TABLE IF NOT EXISTS highscore"
            "(score int, player text, date text)"
        )
        self.db_curs.execute(query)
        self.db_conn.commit()

    def save_highscore(self, score, player="anonymous"):
        try:
            date = time.strftime("%Y/%m/%d")
            query = "INSERT INTO highscore VALUES (?,?,?)"
            self.db_curs.execute(query, (score, player, date))
        except sqlite3.OperationalError as error:
            print(f"GameDatabase.save_highscore(): {error}")
        else:
            self.db_conn.commit()

    def get_highscores(self):
        try:
            query = "SELECT * FROM highscore ORDER BY score DESC LIMIT 10"
            self.db_curs.execute(query)
        except sqlite3.OperationalError as error:
            print(f"GameDatabase.get_highscores(): {error}")
        else:
            self.db_conn.commit()

        return self.db_curs.fetchall()

    def get_highscore_list(self):
        """Returns a list with highscores to display on the screen."""
        num = 1
        x, y = 210, 140
        scores = []
        # Get highscores from the database.
        for score in self.get_highscores():
            text = f"{self._prefix(num)}. {score[0]} {score[1]}"
            scores.append(GenericText(15, text, [x, y]))
            num += 1
            y += 15

        score_list = len(self.get_highscores())
        max_scores = 10
        # Create empty placeholders if there are less than ten scores.
        if score_list < max_scores:
            missing = max_scores - score_list
            for _ in range(missing):
                text = f"{self._prefix(num)}."
                scores.append(GenericText(15, text, [x, y]))
                num += 1
                y += 15

        return scores

    def _prefix(self, num):
        """Prefix single digit numbers with a zero."""
        if num < 10:
            return f"0{num}"
        else:
            return str(num)


class HelpSection:
    def __init__(self, screen, group):

        self.screen = screen
        self.space = group.sprites()  # The scrolling background.
        self.space_group = pygame.sprite.RenderPlain(self.space)

        self.text = [
            GenericText(20, "Mission:", [50, 30]),
            GenericText(15, " Destroy all asteroids", [50, 55]),
            GenericText(15, " and beat the highscore.", [50, 70]),
            GenericText(20, "Points:", [50, 100]),
            GenericText(15, " Shoot = -1 point", [50, 125]),
            GenericText(15, " Asteroid = +100 points", [50, 140]),
            GenericText(15, " Level up = +1000 points", [50, 155]),
            GenericText(20, "Controls:", [50, 185]),
            GenericText(15, " BACKSPACE - Go back", [50, 210]),
            GenericText(15, " ESCAPE - Exit anytime", [50, 225]),
            GenericText(15, " SPACE - Shoot", [50, 240]),
            GenericText(15, " ENTER - Enter", [50, 255]),
            GenericText(15, " ARROWS - Control spaceship", [50, 270]),
            GenericText(15, " P - Pause game", [50, 285]),
        ]
        self.text_group = pygame.sprite.RenderPlain(self.text)

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
                    if event.key == locals.K_BACKSPACE:
                        return

            # Animate space.
            for space in self.space_group.sprites():
                space.animate(pygame.time.get_ticks())

            # Update the screen
            self.space_group.update()
            self.text_group.update()

            # Draw
            self.screen.fill(settings.BG_COLOR)
            self.space_group.draw(self.screen)
            self.text_group.draw(self.screen)

            pygame.display.update()


class GameOver:
    def __init__(self, screen, group):
        self.screen = screen
        self.space = group.sprites()  # The scrolling background.
        self.banner = BannerText(25, "GAME OVER", [0, 50])
        self.title = GenericText(20, "HIGHSCORE:", [250, 100])
        self.highscore = GameDatabase().get_highscore_list()
        self.clock = pygame.time.Clock()
        self.space_group = pygame.sprite.RenderPlain(self.space)
        self.text_group = pygame.sprite.RenderPlain(self.banner, self.title)
        self.sfx = SoundEffect(settings.GAME_OVER, 1.0)

    def update_highscore(self, score):
        """Get an updated version of the highscore list."""
        GameDatabase().save_highscore(score)
        self.text_group.remove(self.highscore)  # Remove old highscore list.
        self.highscore = GameDatabase().get_highscore_list()
        self.text_group.add(self.highscore)

    def run(self, score):

        self.update_highscore(score)

        while True:

            self.clock.tick(settings.FPS)

            for event in pygame.event.get():
                if (
                    event.type == locals.QUIT
                    or event.type == locals.KEYDOWN
                    and event.key == locals.K_ESCAPE
                ):
                    sys.exit()
                if event.type == locals.KEYDOWN:
                    if (
                        event.key == locals.K_RETURN
                        or event.key == locals.K_BACKSPACE
                    ):
                        return

            # Animate space.
            for space in self.space_group.sprites():
                space.animate(pygame.time.get_ticks())

            # Update the screen
            self.space_group.update()
            self.text_group.update()

            # draw space
            self.screen.fill(settings.BG_COLOR)
            self.space_group.draw(self.screen)
            self.text_group.draw(self.screen)

            pygame.display.update()
