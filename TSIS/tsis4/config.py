# ---------- WINDOW ----------
WIDTH, HEIGHT = 700, 600
CELL = 30

# Play area (left part of screen)
PLAY_WIDTH = 600
PLAY_COLS = PLAY_WIDTH // CELL   # 20
PLAY_ROWS = HEIGHT // CELL       # 20

# HUD panel (right strip)
HUD_X = PLAY_WIDTH

# ---------- GAME ----------
FPS_INITIAL = 5
FPS_MAX = 20
LEVEL_UP_SCORE = 4        # score points needed to advance one level
OBSTACLE_START_LEVEL = 3  # obstacles appear from this level onward
OBSTACLES_PER_LEVEL = 3   # extra wall blocks added each level

# ---------- FOOD ----------
FOOD_SPAWN_INTERVAL = 2000   # ms between food spawns
POISON_CHANCE = 0.2           # probability a spawn is poison

# ---------- POWER-UPS ----------
POWERUP_DURATION = 5000       # ms effect lasts
POWERUP_FIELD_LIFETIME = 8000 # ms before it disappears if uncollected
SPEED_BOOST_DELTA = 4         # FPS added / subtracted
POWERUP_TYPES = ["speed", "slow", "shield"]

# ---------- ASSETS ----------
SETTINGS_FILE = "settings.json"