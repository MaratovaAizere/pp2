import pygame
import sys
import datetime
import os

from tools import draw_smooth_line, draw_shape, flood_fill, Button

pygame.init()

WIDTH, HEIGHT = 900, 650
UI_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Paint")

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (220, 50,  50)
GREEN  = (50,  200, 70)
BLUE   = (50,  120, 255)
GRAY   = (200, 200, 200)
DARK   = (80,  80,  80)
PANEL  = (230, 230, 230)

# App state
current_color = BLACK
tool          = "pencil"
drawing       = False
start_pos     = None   # locked anchor for shape tools
last_pos      = None   # last position for pencil/eraser smooth drawing
brush_size    = 5      # current stroke width

# Text tool state
text_active = False
text_pos    = None   # canvas-local position of text cursor
text_buffer = ""     # characters typed so far

canvas = pygame.Surface((WIDTH, HEIGHT - UI_HEIGHT))
canvas.fill(WHITE)

font_ui   = pygame.font.SysFont("Verdana", 14)
font_text = pygame.font.SysFont("Verdana", 20)


# ── Toolbar layout ────────────────────────────────────────────────────────────
ROW1, ROW2 = 8, 52
BH  = 32
BH2 = 26

def btn(x, y, w, h, label, value):
    return Button(x, y, w, h, label, value, font_ui)

tool_buttons = [
    btn(  8, ROW1,  72, BH, "Pencil",  "pencil"),
    btn( 84, ROW1,  56, BH, "Line",    "line"),
    btn(144, ROW1,  56, BH, "Rect",    "rect"),
    btn(204, ROW1,  60, BH, "Circle",  "circle"),
    btn(268, ROW1,  60, BH, "Square",  "square"),
    btn(332, ROW1,  56, BH, "RTri",    "rtri"),
    btn(392, ROW1,  60, BH, "EqTri",   "etri"),
    btn(456, ROW1,  76, BH, "Rhombus", "rhombus"),
    btn(536, ROW1,  60, BH, "Eraser",  "eraser"),
    btn(600, ROW1,  44, BH, "Fill",    "fill"),
    btn(648, ROW1,  48, BH, "Text",    "text"),
    btn(700, ROW1,  56, BH, "Clear",   "clear"),
]

color_buttons = [
    btn(  8, ROW2, 34, BH2, "", RED),
    btn( 46, ROW2, 34, BH2, "", GREEN),
    btn( 84, ROW2, 34, BH2, "", BLUE),
    btn(122, ROW2, 34, BH2, "", BLACK),
]

size_buttons = [
    btn(170, ROW2, 48, BH2, "S (1)", 2),
    btn(222, ROW2, 48, BH2, "M (2)", 5),
    btn(274, ROW2, 52, BH2, "L (3)", 10),
]


# ── Main loop ─────────────────────────────────────────────────────────────────

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ── Key presses ───────────────────────────────────────────────────────
        if event.type == pygame.KEYDOWN:

            # Brush size shortcuts
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            # Save canvas into the "images" folder
            elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                os.makedirs("images", exist_ok=True)
                ts       = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join("images", f"canvas_{ts}.png")
                pygame.image.save(canvas, filename)
                pygame.display.set_caption(f"Saved → {filename}")

            # Text tool input
            elif text_active:
                if event.key == pygame.K_RETURN:
                    # Commit typed text permanently to canvas
                    rendered = font_text.render(text_buffer, True, current_color)
                    canvas.blit(rendered, text_pos)
                    text_active = False
                    text_buffer = ""
                    text_pos    = None
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_buffer = ""
                    text_pos    = None
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                elif event.unicode and event.unicode.isprintable():
                    text_buffer += event.unicode

        # ── Mouse button down ─────────────────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            toolbar_hit = False

            for b in tool_buttons:
                if b.hit((mx, my)):
                    toolbar_hit = True
                    if b.value == "clear":
                        canvas.fill(WHITE)
                        text_active = False
                        text_buffer = ""
                    else:
                        tool = b.value
                        text_active = False

            for b in color_buttons:
                if b.hit((mx, my)):
                    toolbar_hit   = True
                    current_color = b.value

            for b in size_buttons:
                if b.hit((mx, my)):
                    toolbar_hit = True
                    brush_size  = b.value

            # Canvas area click
            if not toolbar_hit and my > UI_HEIGHT:
                cy = my - UI_HEIGHT

                if tool == "fill":
                    flood_fill(canvas, mx, cy, current_color)

                elif tool == "text":
                    # Commit any pending text before moving the cursor
                    if text_active and text_buffer:
                        rendered = font_text.render(text_buffer, True, current_color)
                        canvas.blit(rendered, text_pos)
                    text_active = True
                    text_pos    = (mx, cy)
                    text_buffer = ""

                else:
                    drawing   = True
                    start_pos = (mx, cy)
                    last_pos  = (mx, cy)

        # ── Mouse button up ───────────────────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and tool not in ("pencil", "eraser"):
                ex, ey  = event.pos
                end_pos = (ex, max(0, ey - UI_HEIGHT))
                draw_shape(canvas, tool, start_pos, end_pos, current_color, brush_size)
            drawing = False


    # ── Continuous pencil / eraser ────────────────────────────────────────────
    if drawing and tool in ("pencil", "eraser"):
        mx, my = pygame.mouse.get_pos()
        cy = my - UI_HEIGHT
        if 0 <= cy < HEIGHT - UI_HEIGHT:
            cur   = (mx, cy)
            color = WHITE if tool == "eraser" else current_color
            draw_smooth_line(canvas, color, last_pos, cur, brush_size)
            last_pos = cur


    # ── Render ────────────────────────────────────────────────────────────────
    screen.fill(WHITE)

    # Shape preview while dragging (copy canvas so the preview doesn't persist)
    if drawing and tool not in ("pencil", "eraser") and start_pos is not None:
        mx, my = pygame.mouse.get_pos()
        if my > UI_HEIGHT:
            preview = canvas.copy()
            draw_shape(preview, tool, start_pos, (mx, my - UI_HEIGHT), current_color, brush_size)
            screen.blit(preview, (0, UI_HEIGHT))
        else:
            screen.blit(canvas, (0, UI_HEIGHT))
    else:
        screen.blit(canvas, (0, UI_HEIGHT))

    # Live text preview with blinking cursor
    if text_active and text_pos is not None:
        cursor   = "|" if pygame.time.get_ticks() % 1000 < 500 else ""
        rendered = font_text.render(text_buffer + cursor, True, current_color)
        screen.blit(rendered, (text_pos[0], text_pos[1] + UI_HEIGHT))

    # Toolbar background
    pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, GRAY, (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 1)

    for b in tool_buttons:
        b.draw(screen, tool == b.value)

    for b in color_buttons:
        pygame.draw.rect(screen, b.value, b.rect, border_radius=4)
        if current_color == b.value:
            pygame.draw.rect(screen, WHITE, b.rect, 3, border_radius=4)
            pygame.draw.rect(screen, DARK,  b.rect, 2, border_radius=4)

    for b in size_buttons:
        b.draw(screen, brush_size == b.value)

    # Hint text
    if text_active:
        hint = font_ui.render("Type · Enter = commit · Esc = cancel", True, DARK)
    else:
        hint = font_ui.render("Keys: 1/2/3 = brush size  |  Ctrl+S = save PNG", True, DARK)
    screen.blit(hint, (340, ROW2 + 6))

    pygame.display.flip()
    clock.tick(60)