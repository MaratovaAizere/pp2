# ── Screen ────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
FPS           = 60

# ── Colors ────────────────────────────────────────────────────────────────────
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
RED     = (255, 0,   0)
GREEN   = (0,   200, 0)
BLUE    = (0,   0,   255)
YELLOW  = (255, 215, 0)
ORANGE  = (255, 140, 0)
CYAN    = (0,   220, 220)
GRAY    = (120, 120, 120)
DARK    = (40,  40,  40)
PANEL   = (20,  20,  40)

# ── Road / lane geometry ──────────────────────────────────────────────────────
ROAD_LEFT  = 10    # road edge x
ROAD_RIGHT = 390
LANE_COUNT = 3
LANE_WIDTH = (ROAD_RIGHT - ROAD_LEFT) // LANE_COUNT   # ~126 px per lane
# Lane center x values
LANE_CENTERS = [ROAD_LEFT + LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(LANE_COUNT)]

# ── Coin values ───────────────────────────────────────────────────────────────
COIN_VALUES  = [1, 5, 10]
COIN_COLORS  = {1: (255, 215, 0), 5: (0, 220, 0), 10: (255, 60, 60)}
COIN_RADIUS  = 14

# ── Power-up settings ─────────────────────────────────────────────────────────
POWERUP_TYPES    = ["nitro", "shield", "repair"]
POWERUP_COLORS   = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}
POWERUP_RADIUS   = 16
POWERUP_DURATION = 4000   # ms — nitro and shield last this long on screen if uncollected
NITRO_DURATION   = 4000   # ms active
SHIELD_DURATION  = 0      # until hit (0 = indefinite)

# ── Obstacle settings ─────────────────────────────────────────────────────────
OIL_RADIUS       = 18
POTHOLE_SIZE     = 28
BARRIER_W        = 60
BARRIER_H        = 18

# ── Difficulty scaling ────────────────────────────────────────────────────────
BASE_SPEED          = 5
SPEED_INCREMENT     = 0.5   # added every SPEED_UP_EVERY coins
SPEED_UP_EVERY      = 5
MAX_ENEMIES_START   = 1
ENEMY_ADD_EVERY     = 10    # add one more enemy every N coins

# ── Leaderboard / settings files ─────────────────────────────────────────────
LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE    = "settings.json"

# ── Car color options (must match Player_<color>.png filenames) ───────────────
CAR_COLORS = ["blue", "red", "green", "yellow"]
TOP_N            = 10