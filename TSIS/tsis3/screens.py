import pygame
from constants import *
from ui import Button, TextInput, draw_text, F_TITLE, F_LARGE, F_MED, F_SMALL, F_TINY
from persistence import load_leaderboard, save_settings


def _draw_bg(surface, bg_image):
    """Dim the road background for menu screens."""
    surface.blit(bg_image, (0, 0))
    dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 180))
    surface.blit(dim, (0, 0))


# ── Name Entry ────────────────────────────────────────────────────────────────

def name_entry_screen(surface, clock, bg_image):
    """Prompt the player to enter their name. Returns the entered string."""
    inp = TextInput(SCREEN_WIDTH // 2 - 120, 300, 240, 40, placeholder="Your name")
    btn_start = Button(SCREEN_WIDTH // 2 - 80, 380, 160, 44, "Start")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            inp.handle_event(event)
            if btn_start.is_clicked(event) and inp.text.strip():
                return inp.text.strip()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and inp.text.strip():
                return inp.text.strip()

        _draw_bg(surface, bg_image)
        draw_text(surface, "SPEED RACER", F_TITLE, YELLOW, SCREEN_WIDTH // 2, 160)
        draw_text(surface, "Enter your name", F_MED, WHITE, SCREEN_WIDTH // 2, 270)
        inp.draw(surface)
        btn_start.draw(surface)

        pygame.display.flip()
        clock.tick(FPS)


# ── Main Menu ─────────────────────────────────────────────────────────────────

def main_menu(surface, clock, bg_image):
    """
    Returns one of: "play", "leaderboard", "settings", "quit"
    """
    cx = SCREEN_WIDTH // 2
    buttons = {
        "play":        Button(cx - 90, 220, 180, 46, "Play"),
        "leaderboard": Button(cx - 90, 278, 180, 46, "Leaderboard"),
        "settings":    Button(cx - 90, 336, 180, 46, "Settings"),
        "quit":        Button(cx - 90, 394, 180, 46, "Quit",
                              color=(100, 30, 30), hover_color=(160, 50, 50)),
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for key, btn in buttons.items():
                if btn.is_clicked(event):
                    return key

        _draw_bg(surface, bg_image)
        draw_text(surface, "SPEED RACER", F_TITLE, YELLOW, cx, 140)
        draw_text(surface, "v1.0", F_TINY, GRAY, cx, 185)
        for btn in buttons.values():
            btn.draw(surface)

        pygame.display.flip()
        clock.tick(FPS)


# ── Settings Screen ───────────────────────────────────────────────────────────

def settings_screen(surface, clock, bg_image, settings):
    """
    Mutates and saves settings. Returns when the player clicks Back.
    """
    cx  = SCREEN_WIDTH // 2
    btn_back = Button(cx - 70, 530, 140, 40, "Back")

    car_options   = ["blue", "red", "green", "yellow"]
    diff_options  = ["easy", "normal", "hard"]

    CAR_COLORS_MAP = {"blue": (50, 120, 255), "red": (220, 50, 50), "green": (50, 200, 70), "yellow": (255, 210, 0)}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if btn_back.is_clicked(event):
                save_settings(settings)
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Sound toggle
                if pygame.Rect(cx + 50, 200, 80, 30).collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]

                # Car color cycle
                if pygame.Rect(cx + 50, 270, 80, 30).collidepoint(mx, my):
                    idx = car_options.index(settings["car_color"])
                    settings["car_color"] = car_options[(idx + 1) % len(car_options)]

                # Difficulty cycle
                if pygame.Rect(cx + 50, 340, 80, 30).collidepoint(mx, my):
                    idx = diff_options.index(settings["difficulty"])
                    settings["difficulty"] = diff_options[(idx + 1) % len(diff_options)]

        _draw_bg(surface, bg_image)
        draw_text(surface, "Settings", F_LARGE, YELLOW, cx, 120)

        # Sound
        draw_text(surface, "Sound:", F_MED, WHITE, cx - 60, 215)
        sound_label = "ON" if settings["sound"] else "OFF"
        sound_col   = GREEN if settings["sound"] else RED
        pygame.draw.rect(surface, (50, 50, 80), (cx + 50, 200, 80, 30), border_radius=6)
        draw_text(surface, sound_label, F_MED, sound_col, cx + 90, 215)

        # Car color — label + colored swatch square
        draw_text(surface, "Car:", F_MED, WHITE, cx - 60, 285)
        pygame.draw.rect(surface, (50, 50, 80), (cx + 50, 270, 80, 30), border_radius=6)
        swatch_col = CAR_COLORS_MAP[settings["car_color"]]
        pygame.draw.rect(surface, swatch_col, (cx + 54, 274, 18, 22), border_radius=3)
        draw_text(surface, settings["car_color"].capitalize(), F_MED,
                  swatch_col, cx + 100, 285)

        # Difficulty
        draw_text(surface, "Difficulty:", F_MED, WHITE, cx - 60, 355)
        diff_colors = {"easy": GREEN, "normal": YELLOW, "hard": RED}
        pygame.draw.rect(surface, (50, 50, 80), (cx + 50, 340, 80, 30), border_radius=6)
        draw_text(surface, settings["difficulty"].capitalize(), F_MED,
                  diff_colors[settings["difficulty"]], cx + 90, 355)

        draw_text(surface, "Click boxes to toggle", F_TINY, GRAY, cx, 410)

        btn_back.draw(surface)
        pygame.display.flip()
        clock.tick(FPS)


# ── Leaderboard Screen ────────────────────────────────────────────────────────

def leaderboard_screen(surface, clock, bg_image):
    cx       = SCREEN_WIDTH // 2
    btn_back = Button(cx - 70, 555, 140, 38, "Back")
    entries  = load_leaderboard()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if btn_back.is_clicked(event):
                return

        _draw_bg(surface, bg_image)
        draw_text(surface, "Leaderboard", F_LARGE, YELLOW, cx, 60)

        # Header
        draw_text(surface, "#",      F_TINY, GRAY, 30,  100)
        draw_text(surface, "Name",   F_TINY, GRAY, 120, 100)
        draw_text(surface, "Score",  F_TINY, GRAY, 250, 100)
        draw_text(surface, "Dist m", F_TINY, GRAY, 355, 100)
        pygame.draw.line(surface, GRAY, (10, 112), (390, 112), 1)

        for i, e in enumerate(entries[:10]):
            y   = 128 + i * 40
            col = YELLOW if i == 0 else WHITE
            draw_text(surface, str(i + 1),          F_SMALL, col, 30,  y)
            draw_text(surface, e.get("name","?"),   F_SMALL, col, 130, y)
            draw_text(surface, str(e.get("score",0)), F_SMALL, col, 250, y)
            draw_text(surface, str(e.get("distance",0)), F_SMALL, col, 355, y)

        if not entries:
            draw_text(surface, "No scores yet!", F_MED, GRAY, cx, 300)

        btn_back.draw(surface)
        pygame.display.flip()
        clock.tick(FPS)


# ── Game Over Screen ──────────────────────────────────────────────────────────

def game_over_screen(surface, clock, bg_image, score, distance, coins):
    """
    Shows final stats. Returns "retry" or "menu".
    """
    cx        = SCREEN_WIDTH // 2
    btn_retry = Button(cx - 100, 420, 180, 46, "Retry")
    btn_menu  = Button(cx - 100, 478, 180, 46, "Main Menu",
                       color=(60, 30, 80), hover_color=(100, 50, 130))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if btn_retry.is_clicked(event):
                return "retry"
            if btn_menu.is_clicked(event):
                return "menu"

        _draw_bg(surface, bg_image)
        draw_text(surface, "GAME OVER",  F_TITLE, RED,    cx, 140)
        draw_text(surface, f"Score:    {score}",    F_MED, WHITE,  cx, 240)
        draw_text(surface, f"Distance: {distance}m", F_MED, WHITE,  cx, 275)
        draw_text(surface, f"Coins:    {coins}",    F_MED, YELLOW, cx, 310)

        btn_retry.draw(surface)
        btn_menu.draw(surface)

        pygame.display.flip()
        clock.tick(FPS)