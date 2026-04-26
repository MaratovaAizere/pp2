import pygame
import math
from collections import deque


def get_box(start, end):
    x1, y1 = start
    x2, y2 = end
    return min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)


def draw_smooth_line(surface, color, p1, p2, width):
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    dist = max(1, int(math.hypot(dx, dy)))
    for i in range(dist):
        x = int(p1[0] + dx * i / dist)
        y = int(p1[1] + dy * i / dist)
        pygame.draw.circle(surface, color, (x, y), max(1, width // 2))


def draw_shape(surface, tool, start, end, color, width=2):
    sx, sy = start
    ex, ey = end
    left, top, right, bottom = get_box(start, end)
    w, h = right - left, bottom - top

    if w == 0 and h == 0:
        return

    if tool == "line":
        pygame.draw.line(surface, color, start, end, max(1, width))

    elif tool == "rect":
        if w > 0 and h > 0:
            pygame.draw.rect(surface, color, (left, top, w, h), max(1, width))

    elif tool == "square":
        # Keep the anchor corner fixed; grow in whatever direction the user drags
        size = min(w, h)
        dx = 1 if ex >= sx else -1
        dy = 1 if ey >= sy else -1
        draw_left = min(sx, sx + dx * size)
        draw_top  = min(sy, sy + dy * size)
        pygame.draw.rect(surface, color, (draw_left, draw_top, size, size), max(1, width))

    elif tool == "circle":
        # start is the center; radius = distance to current mouse
        radius = int(math.hypot(ex - sx, ey - sy))
        if radius > 0:
            pygame.draw.circle(surface, color, (sx, sy), radius, max(1, width))

    elif tool == "rtri":
        # Right angle is always at the click anchor; legs go horizontal then vertical
        points = [(sx, sy), (ex, sy), (sx, ey)]
        pygame.draw.polygon(surface, color, points, max(1, width))

    elif tool == "etri":
        # Horizontal base from anchor; apex direction follows vertical drag
        base_len = abs(ex - sx)
        if base_len == 0:
            return
        tri_h    = int(base_len * math.sqrt(3) / 2)
        apex_dir = -1 if ey <= sy else 1
        mid_x    = (sx + ex) // 2
        points   = [(sx, sy), (ex, sy), (mid_x, sy + apex_dir * tri_h)]
        pygame.draw.polygon(surface, color, points, max(1, width))

    elif tool == "rhombus":
        # start = top tip (anchor); drag sets half-width and total height
        half_w = abs(ex - sx)
        full_h = abs(ey - sy)
        dy_dir = 1 if ey >= sy else -1
        if half_w > 0 and full_h > 0:
            points = [
                (sx,          sy),                           # top tip (anchor)
                (sx + half_w, sy + dy_dir * full_h // 2),   # right tip
                (sx,          sy + dy_dir * full_h),         # bottom tip
                (sx - half_w, sy + dy_dir * full_h // 2),   # left tip
            ]
            pygame.draw.polygon(surface, color, points, max(1, width))


def flood_fill(surface, x, y, fill_color):
    target = surface.get_at((x, y))[:3]
    fill   = fill_color[:3]
    if target == fill:
        return

    sw, sh  = surface.get_size()
    visited = set()
    queue   = deque([(x, y)])

    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) in visited:
            continue
        if not (0 <= cx < sw and 0 <= cy < sh):
            continue
        if surface.get_at((cx, cy))[:3] != target:
            continue

        surface.set_at((cx, cy), fill)
        visited.add((cx, cy))
        queue.extend([(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)])


class Button:
    def __init__(self, x, y, w, h, label, value, font):
        self.rect  = pygame.Rect(x, y, w, h)
        self.label = label
        self.value = value
        self.font  = font

    def draw(self, surface, active=False):
        DARK = (80, 80, 80)
        GRAY = (200, 200, 200)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        pygame.draw.rect(surface, DARK if active else GRAY, self.rect, border_radius=4)
        if self.label:
            text = self.font.render(self.label, True, WHITE if active else BLACK)
            tx   = self.rect.x + (self.rect.w - text.get_width())  // 2
            ty   = self.rect.y + (self.rect.h - text.get_height()) // 2
            surface.blit(text, (tx, ty))

    def hit(self, pos):
        return self.rect.collidepoint(pos)