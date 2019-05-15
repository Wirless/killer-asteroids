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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_ROOT = os.path.join(BASE_DIR, 'assets')
FONT_DIR = os.path.join(ASSETS_ROOT, 'font')
DATA_DIR = os.path.join(ASSETS_ROOT, 'data')
AUDIO_DIR = os.path.join(ASSETS_ROOT, 'audio')
IMAGE_DIR = os.path.join(ASSETS_ROOT, 'img')

# The font that will be used in game.
FONT = os.path.join(FONT_DIR, "commodore64.ttf")

# Database for highscores.
DATABASE = os.path.join(DATA_DIR, 'highscore.db')

# Background music.
BG_MUSIC = os.path.join(AUDIO_DIR, "bgmusic.ogg")

# Sound effects.
BEEP = os.path.join(AUDIO_DIR, "beep.wav")
LASER = os.path.join(AUDIO_DIR, "laser.wav")
LEVEL_UP = os.path.join(AUDIO_DIR, "levelup.wav")
GAME_OVER = os.path.join(AUDIO_DIR, "gameover.wav")
COLLISION = os.path.join(AUDIO_DIR, "collision.wav")
EXPLOSION = os.path.join(AUDIO_DIR, "explosion.wav")
POWER_UP = os.path.join(AUDIO_DIR, "powerup.wav")
MENU_BEEP = os.path.join(AUDIO_DIR, "menu_beep.wav")
START_GAME = os.path.join(AUDIO_DIR, "startgame.wav")

# Image files for all the sprites.
POWER_UP_SPRITE = {
    'file': os.path.join(IMAGE_DIR, 'powerup.png'),
    'size': [15, 15]}
POWER_UP_EFFECT_SPRITE = {
    'file': os.path.join(IMAGE_DIR, 'powerupeffect.png'),
    'size': [45, 45]}
ASTEROID_SPRITE = {
    'file': os.path.join(IMAGE_DIR, 'asteroid.png'),
    'size': [35, 35]}
LASER_SPRITE = {
    'file': os.path.join(IMAGE_DIR, 'bluelaser.png',),
    'size': [16, 16]}
EXPLOSION_SPRITE = {
    'file': os.path.join(IMAGE_DIR, 'explosion.png',),
    'size': [64, 64]}
SPACE_SPRITE = {
    'file': os.path.join(IMAGE_DIR, 'space.png',),
    'size': [640, 400]}
PLAYER_SPRITE = {
    'file': os.path.join(IMAGE_DIR, 'spaceship2.png',),
    'size': [92, 36]}
