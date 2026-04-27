"""
main.py — entry point; screen manager + game loop
Screens: MENU → USERNAME → PLAYING → GAME_OVER → LEADERBOARD → SETTINGS
"""

import pygame
import random

import db
import settings as cfg_store
from color_palette import *
from config import (
    WIDTH, HEIGHT, CELL, PLAY_WIDTH, PLAY_COLS, PLAY_ROWS, HUD_X,
    FPS_INITIAL, FPS_MAX, LEVEL_UP_SCORE,
    FOOD_SPAWN_INTERVAL, OBSTACLE_START_LEVEL,
)
from game import (
    Snake, Food, PoisonFood, PowerUp,
    Obstacle, generate_obstacles,
    spawn_food, spawn_powerup,
)

# ───────────────────────────────────────────────
#  Init
# ───────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font_lg = pygame.font.SysFont("Verdana", 28, bold=True)
font_md = pygame.font.SysFont("Verdana", 20)
font_sm = pygame.font.SysFont("Verdana", 15)

db.create_tables()
prefs = cfg_store.load()

# ───────────────────────────────────────────────
#  UI helpers
# ───────────────────────────────────────────────

def txt(surface, text, font, color, cx, cy):
    s = font.render(text, True, color)
    r = s.get_rect(center=(cx, cy))
    surface.blit(s, r)
    return r


def button(surface, text, font, rect, color, hover_color, text_color=colorBLACK):
    mouse = pygame.mouse.get_pos()
    col = hover_color if pygame.Rect(rect).collidepoint(mouse) else color
    pygame.draw.rect(surface, col, rect, border_radius=8)
    pygame.draw.rect(surface, colorWHITE, rect, 2, border_radius=8)
    txt(surface, text, font, text_color, rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)
    return pygame.Rect(rect)


def clicked(rect):
    if pygame.mouse.get_pressed()[0]:
        if rect.collidepoint(pygame.mouse.get_pos()):
            return True
    return False


# ───────────────────────────────────────────────
#  Grid
# ───────────────────────────────────────────────

def draw_grid():
    if not prefs.get("grid_overlay", True):
        return
    for i in range(PLAY_ROWS + 1):
        pygame.draw.line(screen, (40, 40, 40), (0, i * CELL), (PLAY_WIDTH, i * CELL))
    for j in range(PLAY_COLS + 1):
        pygame.draw.line(screen, (40, 40, 40), (j * CELL, 0), (j * CELL, HEIGHT))


# ───────────────────────────────────────────────
#  HUD (right panel)
# ───────────────────────────────────────────────

def draw_hud(score, level, best, snake: Snake):
    pygame.draw.rect(screen, (20, 20, 20), (HUD_X, 0, WIDTH - HUD_X, HEIGHT))
    x = HUD_X + (WIDTH - HUD_X) // 2
    txt(screen, "SNAKE", font_lg, colorGREEN, x, 30)
    txt(screen, f"Score:  {score}", font_md, colorWHITE, x, 80)
    txt(screen, f"Level:  {level}", font_md, colorWHITE, x, 110)
    txt(screen, f"Best:   {best}", font_md, colorGREEN, x, 140)
    txt(screen, f"Length: {len(snake.body)}", font_sm, colorGRAY, x, 170)

    # active effects
    y = 210
    if snake.shield_active:
        txt(screen, "🛡 Shield", font_sm, colorLIGHT_BLUE, x, y); y += 22
    if snake.speed_effect > 0:
        txt(screen, "⚡ Speed+", font_sm, colorCYAN, x, y); y += 22
    elif snake.speed_effect < 0:
        txt(screen, "🐢 Slow", font_sm, colorPURPLE, x, y); y += 22

    # legend
    y = HEIGHT - 160
    txt(screen, "─ Controls ─", font_sm, colorGRAY, x, y); y += 22
    txt(screen, "Arrow keys: move", font_sm, colorGRAY, x, y); y += 20
    txt(screen, "ESC: menu", font_sm, colorGRAY, x, y); y += 22
    txt(screen, "─ Food ─", font_sm, colorGRAY, x, y); y += 20
    for col, label in [(colorGREEN, "x1"), (colorYELLOW, "x2"), (colorORANGE, "x3")]:
        pygame.draw.rect(screen, col, (HUD_X + 10, y - 8, 14, 14))
        txt(screen, label, font_sm, colorWHITE, HUD_X + 55, y); y += 18
    pygame.draw.rect(screen, colorDARK_RED, (HUD_X + 10, y - 8, 14, 14))
    txt(screen, "poison", font_sm, colorWHITE, HUD_X + 55, y)


# ───────────────────────────────────────────────
#  Screen: MENU
# ───────────────────────────────────────────────

def screen_menu():
    BTN_W, BTN_H = 200, 50
    cx = WIDTH // 2
    buttons = {
        "play":        pygame.Rect(cx - BTN_W // 2, 200, BTN_W, BTN_H),
        "leaderboard": pygame.Rect(cx - BTN_W // 2, 270, BTN_W, BTN_H),
        "settings":    pygame.Rect(cx - BTN_W // 2, 340, BTN_W, BTN_H),
        "quit":        pygame.Rect(cx - BTN_W // 2, 410, BTN_W, BTN_H),
    }

    while True:
        screen.fill(colorBLACK)

        # title
        txt(screen, "🐍  SNAKE", font_lg, colorGREEN, cx, 120)
        txt(screen, "Classic arcade game", font_sm, colorGRAY, cx, 155)

        button(screen, "▶  Play", font_md, buttons["play"], colorDARK_GREEN, colorGREEN, colorBLACK)
        button(screen, "🏆  Leaderboard", font_md, buttons["leaderboard"], (30, 30, 80), colorBLUE, colorWHITE)
        button(screen, "⚙  Settings", font_md, buttons["settings"], (60, 40, 0), colorYELLOW, colorBLACK)
        button(screen, "✕  Quit", font_md, buttons["quit"], (80, 0, 0), colorRED, colorWHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttons["play"].collidepoint(event.pos):        return "username"
                if buttons["leaderboard"].collidepoint(event.pos): return "leaderboard"
                if buttons["settings"].collidepoint(event.pos):    return "settings"
                if buttons["quit"].collidepoint(event.pos):        return "quit"

        pygame.display.flip()
        clock.tick(30)


# ───────────────────────────────────────────────
#  Screen: USERNAME
# ───────────────────────────────────────────────

def screen_username():
    username = ""
    error = ""
    BTN = pygame.Rect(WIDTH // 2 - 80, 360, 160, 45)

    while True:
        screen.fill(colorBLACK)
        txt(screen, "Enter your username", font_lg, colorGREEN, WIDTH // 2, 180)
        txt(screen, error, font_sm, colorRED, WIDTH // 2, 220)

        # input box
        box = pygame.Rect(WIDTH // 2 - 140, 250, 280, 50)
        pygame.draw.rect(screen, (30, 30, 30), box, border_radius=6)
        pygame.draw.rect(screen, colorGREEN, box, 2, border_radius=6)
        txt(screen, username + "|", font_md, colorWHITE, WIDTH // 2, 275)

        button(screen, "Confirm", font_md, BTN, colorDARK_GREEN, colorGREEN, colorBLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_RETURN:
                    if username.strip():
                        return username.strip()
                    error = "Username cannot be empty."
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 20:
                    ch = event.unicode
                    if ch.isprintable():
                        username += ch
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BTN.collidepoint(event.pos):
                    if username.strip():
                        return username.strip()
                    error = "Username cannot be empty."

        pygame.display.flip()
        clock.tick(30)


# ───────────────────────────────────────────────
#  Screen: PLAYING
# ───────────────────────────────────────────────

def screen_playing(player_id: int, best_score: int):
    snake_color = tuple(prefs.get("snake_color", [0, 200, 0]))
    snake = Snake(color=snake_color)
    foods: list[Food] = []
    powerup: PowerUp | None = None
    obstacles: list[Obstacle] = []

    score = 0
    level = 1
    base_fps = FPS_INITIAL

    game_state = {}  # shared mutable bag for power-up apply()

    SPAWN_FOOD = pygame.USEREVENT + 1
    SPAWN_PU   = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_FOOD, FOOD_SPAWN_INTERVAL)
    pygame.time.set_timer(SPAWN_PU, 7000)

    running = True
    while running:
        # ── events ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score, level

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  snake.change_direction(1, 0)
                elif event.key == pygame.K_LEFT: snake.change_direction(-1, 0)
                elif event.key == pygame.K_UP:   snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN: snake.change_direction(0, 1)
                elif event.key == pygame.K_ESCAPE:
                    pygame.time.set_timer(SPAWN_FOOD, 0)
                    pygame.time.set_timer(SPAWN_PU, 0)
                    return "menu", score, level

            if event.type == SPAWN_FOOD:
                foods.append(spawn_food(snake, obstacles))

            if event.type == SPAWN_PU and powerup is None:
                powerup = spawn_powerup(snake, obstacles, foods)

        # ── movement ──
        snake.move()
        speed_delta = snake.tick_effects()
        fps = max(1, min(FPS_MAX, base_fps + speed_delta))

        # ── collision ──
        wall_hit = snake.check_wall_collision()
        self_hit = snake.check_self_collision()
        obs_hit  = snake.check_obstacle_collision(obstacles)

        if (wall_hit or self_hit or obs_hit):
            if snake.shield_active:
                snake.shield_active = False
                # push head back inside
                snake.body[0].x = max(0, min(PLAY_COLS - 1, snake.body[0].x))
                snake.body[0].y = max(0, min(PLAY_ROWS - 1, snake.body[0].y))
            else:
                pygame.time.set_timer(SPAWN_FOOD, 0)
                pygame.time.set_timer(SPAWN_PU, 0)
                return "gameover", score, level

        # ── food logic ──
        for f in foods[:]:
            head = snake.head()
            if head.x == f.pos.x and head.y == f.pos.y:
                if isinstance(f, PoisonFood):
                    dead = snake.shrink(2)
                    if dead:
                        pygame.time.set_timer(SPAWN_FOOD, 0)
                        pygame.time.set_timer(SPAWN_PU, 0)
                        return "gameover", score, level
                else:
                    snake.grow()
                    score += f.value
                    # level up
                    new_level = score // LEVEL_UP_SCORE + 1
                    if new_level > level:
                        level = new_level
                        base_fps = min(FPS_MAX, FPS_INITIAL + level - 1)
                        if level >= OBSTACLE_START_LEVEL:
                            obstacles = generate_obstacles(level, snake, obstacles)
                foods.remove(f)
            elif f.is_expired():
                foods.remove(f)

        # ── power-up logic ──
        if powerup is not None:
            head = snake.head()
            if head.x == powerup.pos.x and head.y == powerup.pos.y:
                powerup.apply(snake, game_state)
                powerup = None
            elif powerup.is_expired():
                powerup = None

        # ── draw ──
        screen.fill(colorBLACK)
        draw_grid()

        for o in obstacles:
            o.draw(screen)
        for f in foods:
            f.draw(screen)
        if powerup:
            powerup.draw(screen)
        snake.draw(screen)

        draw_hud(score, level, best_score, snake)

        pygame.display.flip()
        clock.tick(fps)

    return "quit", score, level


# ───────────────────────────────────────────────
#  Screen: GAME OVER
# ───────────────────────────────────────────────

def screen_gameover(score: int, level: int, best_score: int):
    BTN_W, BTN_H = 180, 48
    cx = WIDTH // 2
    BTN_RETRY = pygame.Rect(cx - BTN_W - 20, 400, BTN_W, BTN_H)
    BTN_MENU  = pygame.Rect(cx + 20,          400, BTN_W, BTN_H)

    personal_best = max(score, best_score)

    while True:
        screen.fill(colorBLACK)
        txt(screen, "GAME OVER", font_lg, colorRED, cx, 160)
        txt(screen, f"Score:  {score}", font_md, colorWHITE, cx, 220)
        txt(screen, f"Level:  {level}", font_md, colorWHITE, cx, 255)
        txt(screen, f"Best:   {personal_best}", font_md, colorGREEN, cx, 290)

        button(screen, "▶ Retry",    font_md, BTN_RETRY, colorDARK_GREEN, colorGREEN, colorBLACK)
        button(screen, "⌂ Menu",     font_md, BTN_MENU,  (30, 30, 80),    colorBLUE,  colorWHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BTN_RETRY.collidepoint(event.pos): return "play"
                if BTN_MENU.collidepoint(event.pos):  return "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return "play"
                if event.key == pygame.K_ESCAPE: return "menu"

        pygame.display.flip()
        clock.tick(30)


# ───────────────────────────────────────────────
#  Screen: LEADERBOARD
# ───────────────────────────────────────────────

def screen_leaderboard():
    BTN_BACK = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 70, 160, 45)
    rows = db.get_top_scores(10)

    while True:
        screen.fill(colorBLACK)
        txt(screen, "🏆  Leaderboard", font_lg, colorYELLOW, WIDTH // 2, 40)

        # header
        pygame.draw.line(screen, colorGRAY, (40, 70), (WIDTH - 40, 70))
        hdr = ["#", "Player", "Score", "Level", "Date"]
        cols_x = [60, 140, 330, 430, 520]
        for hx, ht in zip(cols_x, hdr):
            txt(screen, ht, font_sm, colorGRAY, hx, 85)
        pygame.draw.line(screen, colorGRAY, (40, 100), (WIDTH - 40, 100))

        # rows
        for i, row in enumerate(rows):
            name, sc, lvl, date = row
            y = 120 + i * 28
            row_col = colorYELLOW if i == 0 else colorWHITE
            for hx, val in zip(cols_x, [str(i + 1), name, str(sc), str(lvl), date]):
                txt(screen, val, font_sm, row_col, hx, y)

        button(screen, "← Back", font_md, BTN_BACK, (30, 30, 80), colorBLUE, colorWHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BTN_BACK.collidepoint(event.pos): return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(30)


# ───────────────────────────────────────────────
#  Screen: SETTINGS
# ───────────────────────────────────────────────

_COLOR_OPTIONS = [
    ("Green",  [0, 200, 0]),
    ("Lime",   [100, 255, 50]),
    ("Blue",   [0, 100, 255]),
    ("Cyan",   [0, 220, 220]),
    ("Yellow", [255, 220, 0]),
    ("Orange", [255, 140, 0]),
    ("Pink",   [255, 105, 180]),
    ("White",  [220, 220, 220]),
]

SWATCH = 44   # size of each colour swatch
SWATCH_GAP = 10


def _draw_toggle(surface, label, enabled: bool, rect: pygame.Rect) -> None:
    """Draw a labelled toggle row: label on the left, ON/OFF pill on the right."""
    # row background
    pygame.draw.rect(surface, (25, 25, 25), rect, border_radius=8)
    pygame.draw.rect(surface, (60, 60, 60), rect, 1, border_radius=8)

    # label
    lbl_surf = font_md.render(label, True, colorWHITE)
    surface.blit(lbl_surf, (rect.x + 16, rect.centery - lbl_surf.get_height() // 2))

    # pill
    pill_w, pill_h = 70, 28
    pill_x = rect.right - pill_w - 16
    pill_y = rect.centery - pill_h // 2
    pill_rect = pygame.Rect(pill_x, pill_y, pill_w, pill_h)
    pill_color = colorDARK_GREEN if enabled else (80, 0, 0)
    pygame.draw.rect(surface, pill_color, pill_rect, border_radius=14)
    pill_lbl = font_sm.render("ON" if enabled else "OFF", True, colorWHITE)
    surface.blit(pill_lbl, pill_lbl.get_rect(center=pill_rect.center))


def _draw_snake_preview(surface, color: list, cx: int, cy: int) -> None:
    """Draw a tiny 5-segment snake preview using the chosen colour."""
    segs = [(cx + (2 - i) * 18, cy) for i in range(5)]
    # body
    for i, (sx, sy) in enumerate(segs[1:], 1):
        pygame.draw.rect(surface, tuple(color), (sx - 8, sy - 8, 16, 16), border_radius=3)
    # head in red
    pygame.draw.rect(surface, colorRED, (segs[0][0] - 9, segs[0][1] - 9, 18, 18), border_radius=4)


def screen_settings():
    local = dict(prefs)  # work on a copy
    cx = WIDTH // 2

    # ── layout constants ──
    PANEL_W = 460
    panel_x = cx - PANEL_W // 2

    TOGGLE_H = 52
    grid_rect  = pygame.Rect(panel_x, 110, PANEL_W, TOGGLE_H)
    sound_rect = pygame.Rect(panel_x, 175, PANEL_W, TOGGLE_H)

    # colour swatches — centred
    total_sw = len(_COLOR_OPTIONS) * SWATCH + (len(_COLOR_OPTIONS) - 1) * SWATCH_GAP
    sw_start_x = cx - total_sw // 2

    BTN_SAVE = pygame.Rect(cx - 100, HEIGHT - 72, 200, 48)

    while True:
        screen.fill((12, 12, 18))   # deep navy, less harsh than pure black

        # ── title ──
        txt(screen, "Settings", font_lg, colorYELLOW, cx, 55)
        pygame.draw.line(screen, (60, 60, 60), (panel_x, 85), (panel_x + PANEL_W, 85))

        # ── toggles ──
        _draw_toggle(screen, "Grid overlay", local["grid_overlay"], grid_rect)
        _draw_toggle(screen, "Sound",        local["sound"],        sound_rect)

        # ── colour section header ──
        txt(screen, "Snake colour", font_md, colorGRAY, cx, 248)

        # ── swatches ──
        swatch_rects = []
        for i, (name, rgb) in enumerate(_COLOR_OPTIONS):
            sx = sw_start_x + i * (SWATCH + SWATCH_GAP)
            sy = 265
            sr = pygame.Rect(sx, sy, SWATCH, SWATCH)

            selected = (local["snake_color"] == rgb)

            # glow behind selected
            if selected:
                glow = sr.inflate(8, 8)
                pygame.draw.rect(screen, tuple(rgb), glow, border_radius=10)

            pygame.draw.rect(screen, tuple(rgb), sr, border_radius=7)

            # white border on selected, dim border otherwise
            border_col = colorWHITE if selected else (80, 80, 80)
            pygame.draw.rect(screen, border_col, sr, 2, border_radius=7)

            # name label below
            lbl = font_sm.render(name, True, colorWHITE if selected else colorGRAY)
            screen.blit(lbl, lbl.get_rect(centerx=sr.centerx, top=sr.bottom + 4))

            swatch_rects.append((sr, rgb))

        # ── snake preview ──
        preview_y = 370
        txt(screen, "Preview:", font_sm, colorGRAY, cx, preview_y - 16)
        # dark box
        preview_box = pygame.Rect(cx - 60, preview_y - 2, 120, 32)
        pygame.draw.rect(screen, (20, 20, 20), preview_box, border_radius=6)
        pygame.draw.rect(screen, (50, 50, 50), preview_box, 1, border_radius=6)
        _draw_snake_preview(screen, local["snake_color"], cx, preview_y + 13)

        # ── save button ──
        mouse = pygame.mouse.get_pos()
        btn_hover = BTN_SAVE.collidepoint(mouse)
        btn_col = colorGREEN if btn_hover else colorDARK_GREEN
        pygame.draw.rect(screen, btn_col, BTN_SAVE, border_radius=10)
        pygame.draw.rect(screen, colorWHITE, BTN_SAVE, 2, border_radius=10)
        txt(screen, "Save & Back", font_md, colorBLACK, BTN_SAVE.centerx, BTN_SAVE.centery)

        # ── hint ──
        txt(screen, "ESC — back without saving", font_sm, (70, 70, 70), cx, HEIGHT - 18)

        # ── events ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return   # discard changes

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                if grid_rect.collidepoint(pos):
                    local["grid_overlay"] = not local["grid_overlay"]

                elif sound_rect.collidepoint(pos):
                    local["sound"] = not local["sound"]

                elif BTN_SAVE.collidepoint(pos):
                    prefs.update(local)
                    cfg_store.save(prefs)
                    return

                else:
                    for sr, rgb in swatch_rects:
                        if sr.collidepoint(pos):
                            local["snake_color"] = rgb
                            break

        pygame.display.flip()
        clock.tick(30)


# ───────────────────────────────────────────────
#  Main state-machine
# ───────────────────────────────────────────────

def main():
    state = "menu"
    player_id = None
    best_score = 0
    last_score = 0
    last_level = 1

    while state != "quit":
        # ── MENU ──
        if state == "menu":
            state = screen_menu()

        # ── USERNAME ──
        elif state == "username":
            username = screen_username()
            if username is None:
                state = "menu"
            else:
                player_id = db.get_or_create_player(username)
                best_score = db.get_best_score(player_id)
                state = "play"

        # ── PLAY ──
        elif state == "play":
            result, last_score, last_level = screen_playing(player_id, best_score)
            if result == "gameover":
                db.save_game(player_id, last_score, last_level)
                best_score = max(best_score, last_score)
                state = "gameover"
            elif result == "menu":
                state = "menu"
            else:
                state = "quit"

        # ── GAME OVER ──
        elif state == "gameover":
            decision = screen_gameover(last_score, last_level, best_score)
            state = decision   # "play" / "menu" / "quit"

        # ── LEADERBOARD ──
        elif state == "leaderboard":
            screen_leaderboard()
            state = "menu"

        # ── SETTINGS ──
        elif state == "settings":
            screen_settings()
            state = "menu"

        else:
            state = "quit"

    pygame.quit()


if __name__ == "__main__":
    main()