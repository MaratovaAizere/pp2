"""
main.py — entry point for Speed Racer.
"""

import pygame, sys, os
from persistence import load_settings, save_settings, save_leaderboard
from racer import (
    SCREEN_W, SCREEN_H, FPS_CAP, CAR_COLORS,
    name_entry_screen, main_menu, settings_screen,
    leaderboard_screen, game_over_screen, run_game,
)

# ── Init ──────────────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

surface = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Speed Racer")
clock = pygame.time.Clock()

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

# ── Assets ────────────────────────────────────────────────────────────────────
bg_image    = pygame.image.load(os.path.join(ASSETS, "AnimatedStreet.png")).convert()
enemy_image = pygame.image.load(os.path.join(ASSETS, "Enemy.png")).convert_alpha()

player_images = {
    c: pygame.image.load(os.path.join(ASSETS, f"Player_{c}.png")).convert_alpha()
    for c in CAR_COLORS
}

try:
    crash_sound = pygame.mixer.Sound(os.path.join(ASSETS, "crash.wav"))
except Exception:
    crash_sound = None

# ── Settings & username ───────────────────────────────────────────────────────
settings = load_settings()
username = name_entry_screen(surface, clock, bg_image)

# ── Main loop ─────────────────────────────────────────────────────────────────
while True:
    choice = main_menu(surface, clock, bg_image)

    if choice == "quit":
        pygame.quit()
        sys.exit()

    elif choice == "settings":
        settings_screen(surface, clock, bg_image, settings, save_settings)

    elif choice == "leaderboard":
        leaderboard_screen(surface, clock, bg_image)

    elif choice == "play":
        while True:
            result = run_game(
                surface, clock, bg_image, player_images,
                enemy_image, crash_sound, settings, username,
                assets_dir=ASSETS,
            )

            save_leaderboard({
                "name":     username,
                "score":    result["score"],
                "distance": result["distance"],
                "coins":    result["coins"],
            })

            action = game_over_screen(
                surface, clock, bg_image,
                result["score"], result["distance"], result["coins"],
            )

            if action == "retry":
                continue
            break