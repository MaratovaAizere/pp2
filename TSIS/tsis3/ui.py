"""
ui.py — shared UI primitives: fonts, Button, TextInput, HUD, draw helpers.
"""

import pygame

# ── Constants (inline to avoid circular imports) ──────────────────────────────
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (120, 120, 120)
DARK   = (40,  40,  40)
YELLOW = (255, 215, 0)
GREEN  = (0,   200, 0)
RED    = (255, 0,   0)
CYAN   = (0,   220, 220)

# ── Fonts ─────────────────────────────────────────────────────────────────────
pygame.font.init()
F_TITLE = pygame.font.SysFont("Verdana", 36, bold=True)
F_LARGE = pygame.font.SysFont("Verdana", 28, bold=True)
F_MED   = pygame.font.SysFont("Verdana", 20)
F_SMALL = pygame.font.SysFont("Verdana", 15)
F_TINY  = pygame.font.SysFont("Verdana", 13)


# ── Helpers ───────────────────────────────────────────────────────────────────

def draw_text(surface, text, font, color, cx, cy):
    """Blit text centred at (cx, cy)."""
    surf = font.render(str(text), True, color)
    surface.blit(surf, (cx - surf.get_width() // 2,
                        cy - surf.get_height() // 2))


def draw_bg(surface, bg_image):
    """Dim the road background for menu/overlay screens."""
    surface.blit(bg_image, (0, 0))
    dim = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 175))
    surface.blit(dim, (0, 0))


# ── Button ────────────────────────────────────────────────────────────────────

class Button:
    def __init__(self, x, y, w, h, label,
                 color=(55, 55, 100), hover_color=(85, 85, 155),
                 text_color=WHITE):
        self.rect        = pygame.Rect(x, y, w, h)
        self.label       = label
        self.color       = color
        self.hover_color = hover_color
        self.text_color  = text_color

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        col = self.hover_color if hovered else self.color
        pygame.draw.rect(surface, col,   self.rect, border_radius=9)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=9)
        draw_text(surface, self.label, F_MED, self.text_color,
                  self.rect.centerx, self.rect.centery)

    def is_clicked(self, event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


# ── TextInput ─────────────────────────────────────────────────────────────────

class TextInput:
    def __init__(self, x, y, w, h, placeholder="", max_len=16):
        self.rect        = pygame.Rect(x, y, w, h)
        self.text        = ""
        self.placeholder = placeholder
        self.active      = False
        self.max_len     = max_len

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.active = False
            elif len(self.text) < self.max_len and event.unicode.isprintable():
                self.text += event.unicode

    def draw(self, surface):
        border = WHITE if self.active else GRAY
        pygame.draw.rect(surface, DARK, self.rect, border_radius=6)
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=6)
        display = self.text + ("|" if self.active else "") if self.text else self.placeholder
        color   = WHITE if self.text else GRAY
        surf = F_MED.render(display, True, color)
        surface.blit(surf, (self.rect.x + 8,
                            self.rect.centery - surf.get_height() // 2))


# ── HUD ───────────────────────────────────────────────────────────────────────

def draw_hud(surface, score, coins, distance, shield, nitro,
             nitro_ms_left, powerup_label):
    """Transparent top bar with game stats."""
    bar = pygame.Surface((surface.get_width(), 52), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 145))
    surface.blit(bar, (0, 0))

    draw_text(surface, f"Score: {score}", F_SMALL, WHITE,  60,  14)
    draw_text(surface, f"Coins: {coins}", F_SMALL, WHITE,  60,  34)
    draw_text(surface, f"Dist: {distance}m", F_SMALL, WHITE, 200, 14)

    if powerup_label:
        label = powerup_label
        if nitro_ms_left > 0:
            label += f" {nitro_ms_left // 1000 + 1}s"
        draw_text(surface, label, F_SMALL, YELLOW, 320, 14)

    if shield:
        draw_text(surface, "Shield", F_TINY, CYAN, 320, 34)