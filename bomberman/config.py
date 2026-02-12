# config.py - Game Configuration Settings
import os

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 40

# Game Grid Settings
GRID_WIDTH = 15
GRID_HEIGHT = 13

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player Settings
PLAYER_SPEED = 3
INITIAL_BOMB_COUNT = 1
INITIAL_BOMB_POWER = 1
BOMB_TIMER = 3000  # milliseconds

# Database Settings (supports both local and Docker environments)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'myrootpass'),
    'database': os.getenv('DB_NAME', 'bomberman_db')
}

# Network Settings
SERVER_HOST = os.getenv('SERVER_HOST', '192.168.208.1')  # Listen on all interfaces
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))

# Theme Settings
THEMES = {
    'desert': {
        'bg_color': (194, 178, 128),
        'breakable_color': (160, 82, 45),
        'unbreakable_color': (139, 69, 19),
        'hard_color': (205, 133, 63)
    },
    'forest': {
        'bg_color': (34, 139, 34),
        'breakable_color': (0, 100, 0),
        'unbreakable_color': (47, 79, 47),
        'hard_color': (85, 107, 47)
    },
    'city': {
        'bg_color': (128, 128, 128),
        'breakable_color': (169, 169, 169),
        'unbreakable_color': (105, 105, 105),
        'hard_color': (112, 128, 144)
    }
}

# PowerUp Settings
POWERUP_TYPES = ['bomb_count', 'bomb_power', 'speed_boost']
POWERUP_SPAWN_CHANCE = 0.5  # 50% şans - daha sık powerup spawn olsun

# Enemy Settings
ENEMY_SPEED = 2
ENEMY_TYPES = ['static', 'chasing', 'intelligent']