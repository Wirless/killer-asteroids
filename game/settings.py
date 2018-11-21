import os.path

# Maximum frames per seconds.
FPS = 30

# The screens width & height.
WIDTH = 640
HEIGHT = 400

LIMIT_UP = 35
LIMIT_DOWN = HEIGHT-40
LIMIT_LEFT = 0
LIMIT_RIGHT = WIDTH-100

# The name of the game.
CAPTION = "KILLER ASTEROIDS"

# The background color.
BG_COLOR = (0, 0, 15)
TEXT_COLOR = (255, 255, 255)
ACTIVE_OPTION = (0, 255, 0)

# The font that will be used in game.
FONT = os.path.join('assets', 'font', "commodore64.ttf")

# Database for highscores.
DATABASE = os.path.join('data', 'highscore.db')

# Background music.
BG_MUSIC = os.path.join('assets', 'audio', "bgmusic.ogg")

# Sound effects.
BEEP = os.path.join('assets', 'audio', "beep.wav")
LASER = os.path.join('assets', 'audio', "laser.wav")
LEVEL_UP = os.path.join('assets', 'audio', "levelup.wav")
GAME_OVER = os.path.join('assets', 'audio', "gameover.wav")
COLLISION = os.path.join('assets', 'audio', "collision.wav")
EXPLOSION = os.path.join('assets', 'audio', "explosion.wav")
POWER_UP = os.path.join('assets', 'audio', "powerup.wav")
MENU_BEEP = os.path.join('assets', 'audio', "menu_beep.wav")
START_GAME = os.path.join('assets', 'audio', "startgame.wav")

# Image files for all the sprites.
POWER_UP_SPRITE = {
    'file': os.path.join('assets', 'img', 'powerup.png'),
    'size': [15, 15]}
POWER_UP_EFFECT_SPRITE = {
    'file': os.path.join('assets', 'img', 'powerupeffect.png'),
    'size': [45, 45]}
ASTEROID_SPRITE = {
    'file': os.path.join('assets', 'img', 'asteroid.png'),
    'size': [35, 35]}
LASER_SPRITE = {
    'file': os.path.join('assets', 'img', 'bluelaser.png',),
    'size': [16, 16]}
EXPLOSION_SPRITE = {
    'file': os.path.join('assets', 'img', 'explosion.png',),
    'size': [64, 64]}
SPACE_SPRITE = {
    'file': os.path.join('assets', 'img', 'space.png',),
    'size': [640, 400]}
PLAYER_SPRITE = {
    'file': os.path.join('assets', 'img', 'spaceship2.png',),
    'size': [92, 36]}
