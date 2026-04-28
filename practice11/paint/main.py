import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
UI_HEIGHT = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Paint UI")

# ---------- COLORS ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (220, 50, 50)
GREEN = (50, 200, 70)
BLUE  = (50, 120, 255)
GRAY  = (200, 200, 200)
DARK  = (80, 80, 80)

# ---------- STATE ----------
current_color = BLACK
tool          = "pen"
drawing       = False
start_pos     = None
last_pos      = None

brush_size  = 6
eraser_size = 16

canvas = pygame.Surface((WIDTH, HEIGHT - UI_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Verdana", 13)

# ---------- BUTTON CLASS ----------
class Button:
    def __init__(self, x, y, w, h, text, value):
        self.rect  = pygame.Rect(x, y, w, h)
        self.text  = text
        self.value = value

    def draw(self, surface, active=False):
        pygame.draw.rect(surface, DARK if active else GRAY, self.rect)
        label = font.render(self.text, True, WHITE if active else BLACK)
        # Center the label inside the button
        tx = self.rect.x + (self.rect.w - label.get_width())  // 2
        ty = self.rect.y + (self.rect.h - label.get_height()) // 2
        surface.blit(label, (tx, ty))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------- UI BUTTONS ----------
# Row 1: original tools + 4 new shapes
tool_buttons = [
    Button( 10, 10,  60, 30, "Pen",     "pen"),
    Button( 75, 10,  60, 30, "Rect",    "rect"),
    Button(140, 10,  65, 30, "Circle",  "circle"),
    Button(210, 10,  65, 30, "Eraser",  "eraser"),
    # ── new shapes ──
    Button(280, 10,  65, 30, "Square",  "square"),
    Button(350, 10,  70, 30, "RTri",    "rtri"),
    Button(425, 10,  70, 30, "EqTri",   "etri"),
    Button(500, 10,  78, 30, "Rhombus", "rhombus"),
    Button(585, 10,  60, 30, "Clear",   "clear"),
]

# Row 2: color swatches (drawn manually, not as text buttons)
color_buttons = [
    Button( 10, 46, 40, 25, "", RED),
    Button( 55, 46, 40, 25, "", GREEN),
    Button(100, 46, 40, 25, "", BLUE),
    Button(145, 46, 40, 25, "", BLACK),
]

# ---------- HELPERS ----------
def draw_smooth_line(surface, color, start, end, width):
    """Stamp small circles along the segment for a smooth stroke."""
    dx   = end[0] - start[0]
    dy   = end[1] - start[1]
    dist = max(1, int(math.hypot(dx, dy)))
    for i in range(dist):
        x = int(start[0] + dx * i / dist)
        y = int(start[1] + dy * i / dist)
        pygame.draw.circle(surface, color, (x, y), width)


def draw_shape(surface, tool, start, end, color):
    """Draw one of the shape tools onto surface using start as the anchor."""
    sx, sy = start
    ex, ey = end

    if tool == "rect":
        # Bounding box rectangle
        left   = min(sx, ex);  top    = min(sy, ey)
        right  = max(sx, ex);  bottom = max(sy, ey)
        pygame.draw.rect(surface, color, (left, top, right-left, bottom-top), 2)

    elif tool == "square":
        # Square anchored at start; side = smaller of the two drag distances
        w    = abs(ex - sx)
        h    = abs(ey - sy)
        side = min(w, h)
        # Grow in the direction the user dragged
        dx   = 1 if ex >= sx else -1
        dy   = 1 if ey >= sy else -1
        pygame.draw.rect(surface, color,
                         (min(sx, sx + dx*side), min(sy, sy + dy*side), side, side), 2)

    elif tool == "circle":
        # start is the center; radius = distance to mouse
        radius = int(math.hypot(ex - sx, ey - sy))
        if radius > 0:
            pygame.draw.circle(surface, color, (sx, sy), radius, 2)

    elif tool == "rtri":
        # Right angle pinned at start; legs run horizontally and vertically
        points = [(sx, sy), (ex, sy), (sx, ey)]
        pygame.draw.polygon(surface, color, points, 2)

    elif tool == "etri":
        # Horizontal base from start to (ex, sy); apex above/below by correct height
        base_len = abs(ex - sx)
        if base_len == 0:
            return
        tri_h    = int(base_len * math.sqrt(3) / 2)
        apex_dir = -1 if ey <= sy else 1          # drag up → apex above base
        mid_x    = (sx + ex) // 2
        points   = [(sx, sy), (ex, sy), (mid_x, sy + apex_dir * tri_h)]
        pygame.draw.polygon(surface, color, points, 2)

    elif tool == "rhombus":
        # start = top tip; drag right sets half-width, drag down sets height
        half_w = abs(ex - sx)
        full_h = abs(ey - sy)
        if half_w == 0 or full_h == 0:
            return
        dy_dir = 1 if ey >= sy else -1
        points = [
            (sx,           sy),                          # top tip (anchor)
            (sx + half_w,  sy + dy_dir * full_h // 2),  # right tip
            (sx,           sy + dy_dir * full_h),        # bottom tip
            (sx - half_w,  sy + dy_dir * full_h // 2),  # left tip
        ]
        pygame.draw.polygon(surface, color, points, 2)


# ---------- MAIN LOOP ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------- MOUSE DOWN ----------
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            for btn in tool_buttons:
                if btn.is_clicked((x, y)):
                    if btn.value == "clear":
                        canvas.fill(WHITE)
                    else:
                        tool = btn.value

            for btn in color_buttons:
                if btn.is_clicked((x, y)):
                    current_color = btn.value

            if y > UI_HEIGHT:
                drawing   = True
                start_pos = (x, y - UI_HEIGHT)
                last_pos  = start_pos

        # ---------- MOUSE UP ----------
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and tool not in ("pen", "eraser"):
                end_pos = (event.pos[0], max(0, event.pos[1] - UI_HEIGHT))
                draw_shape(canvas, tool, start_pos, end_pos, current_color)
            drawing = False

    # ---------- CONTINUOUS PEN / ERASER ----------
    if drawing:
        mx, my = pygame.mouse.get_pos()
        my -= UI_HEIGHT
        if my >= 0:
            cur = (mx, my)
            if tool == "pen":
                draw_smooth_line(canvas, current_color, last_pos, cur, brush_size)
            elif tool == "eraser":
                draw_smooth_line(canvas, WHITE, last_pos, cur, eraser_size)
            last_pos = cur

    # ---------- RENDER ----------
    screen.fill(WHITE)
    screen.blit(canvas, (0, UI_HEIGHT))

    # Live shape preview (drawn on a copy so it doesn't burn into the canvas)
    if drawing and tool not in ("pen", "eraser") and start_pos is not None:
        mx, my = pygame.mouse.get_pos()
        if my > UI_HEIGHT:
            preview = canvas.copy()
            draw_shape(preview, tool, start_pos, (mx, my - UI_HEIGHT), current_color)
            screen.blit(preview, (0, UI_HEIGHT))

    # Toolbar background
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, UI_HEIGHT))

    for btn in tool_buttons:
        btn.draw(screen, tool == btn.value)

    # Color swatches with active highlight
    for btn in color_buttons:
        pygame.draw.rect(screen, btn.value, btn.rect)
        if current_color == btn.value:
            pygame.draw.rect(screen, WHITE, btn.rect, 3)
            pygame.draw.rect(screen, DARK,  btn.rect, 2)

    pygame.display.update()