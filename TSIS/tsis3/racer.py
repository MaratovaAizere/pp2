"""
racer.py — sprites, safe-spawn registry, game loop, and all Pygame screens.

Safe-spawn registry
───────────────────
Every live object registers its bounding rect. Before any new object is
placed it checks the registry so nothing spawns on top of anything else.
Objects deregister themselves when they leave the screen or are collected.
"""

import pygame, random, os
from ui import (draw_bg, draw_hud, draw_text,
                Button, TextInput,
                F_TITLE, F_LARGE, F_MED, F_SMALL, F_TINY,
                WHITE, BLACK, GRAY, DARK, YELLOW, GREEN, RED, CYAN)

# ── Geometry / constants ──────────────────────────────────────────────────────
SCREEN_W  = 400
SCREEN_H  = 600
FPS_CAP   = 60

ROAD_LEFT  = 10
ROAD_RIGHT = 390
LANE_COUNT = 3
LANE_W     = (ROAD_RIGHT - ROAD_LEFT) // LANE_COUNT
LANE_CX    = [ROAD_LEFT + LANE_W * i + LANE_W // 2 for i in range(LANE_COUNT)]

ORANGE = (255, 140, 0)
BLUE   = (0,   0,   255)

COIN_VALUES  = [1, 5, 10]
COIN_COLORS  = {1: (255, 215, 0), 5: (0, 220, 0), 10: (255, 60, 60)}
COIN_R       = 14

PU_TYPES    = ["nitro", "shield", "repair"]
PU_COLORS   = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}
PU_R        = 16
PU_TIMEOUT  = 12_000   # ms before uncollected power-up disappears

NITRO_DUR   = 4_000    # ms
SLOW_DUR    = 2_000    # ms

BASE_SPEED      = 5
SPEED_INC       = 0.5
SPEED_UP_EVERY  = 5
ENEMY_ADD_EVERY = 10
MAX_ENEMIES     = 4

DIFF_MULT = {"easy": 0.7, "normal": 1.0, "hard": 1.5}

CAR_COLORS = ["blue", "red", "green", "yellow"]


# ═════════════════════════════════════════════════════════════════════════════
#  Safe-spawn registry
# ═════════════════════════════════════════════════════════════════════════════

class SpawnRegistry:
    """
    Tracks the axis-aligned bounding rects of every live object.
    Before placing a new object call `is_clear(rect)` — it returns True
    only when the proposed rect does not overlap anything registered AND
    does not overlap the player.
    """

    def __init__(self):
        self._rects: list[pygame.Rect] = []

    def clear(self):
        self._rects.clear()

    def register(self, rect: pygame.Rect):
        self._rects.append(rect.copy())

    def is_clear(self, rect: pygame.Rect, margin: int = 8) -> bool:
        grown = rect.inflate(margin * 2, margin * 2)
        return not any(grown.colliderect(r) for r in self._rects)

    def rebuild(self, objects):
        """Re-snapshot all live objects each frame (call once per frame)."""
        self._rects.clear()
        for obj in objects:
            r = obj.get_rect() if hasattr(obj, "get_rect") else obj.rect
            self._rects.append(r.copy())


def _safe_lane_place(registry: SpawnRegistry,
                     w: int, h: int, margin: int = 8,
                     y_override: int | None = None,
                     tries: int = 30) -> tuple[int, int] | None:
    """
    Try up to `tries` times to find a lane centre x and y=-h (or y_override)
    that does not collide with anything in the registry.
    Returns (cx, y) or None if no free slot found.
    """
    for _ in range(tries):
        cx = random.choice(LANE_CX)
        y  = y_override if y_override is not None else -h
        r  = pygame.Rect(cx - w // 2, y, w, h)
        if registry.is_clear(r, margin):
            return cx, y
    return None


# ═════════════════════════════════════════════════════════════════════════════
#  Sprites / objects
# ═════════════════════════════════════════════════════════════════════════════

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image      = image.copy()
        self.rect       = self.image.get_rect(center=(SCREEN_W // 2, 520))
        self.shield     = False
        self.nitro      = False
        self.slowed     = False
        self.nitro_end  = 0
        self.slow_end   = 0
        self.base_speed = BASE_SPEED
        self.speed      = self.base_speed

    def get_rect(self): return self.rect

    def move(self):
        keys = pygame.key.get_pressed()
        spd  = max(2, self.speed // 2) if self.slowed else self.speed
        if keys[pygame.K_LEFT]  and self.rect.left  > ROAD_LEFT:
            self.rect.x -= spd
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += spd

    def activate_nitro(self):
        self.nitro     = True
        self.slowed    = False
        self.speed     = self.base_speed * 2
        self.nitro_end = pygame.time.get_ticks() + NITRO_DUR

    def activate_slow(self):
        if not self.nitro:
            self.slowed   = True
            self.slow_end = pygame.time.get_ticks() + SLOW_DUR

    def set_base_speed(self, s):
        self.base_speed = s
        if not self.nitro:
            self.speed = s

    def update_powerups(self):
        now = pygame.time.get_ticks()
        if self.nitro and now >= self.nitro_end:
            self.nitro = False
            self.speed = self.base_speed
        if self.slowed and now >= self.slow_end:
            self.slowed = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed, registry: SpawnRegistry):
        super().__init__()
        self.image    = image.copy()
        self.rect     = self.image.get_rect()
        self.speed    = speed
        self._place(registry, start_offscreen=True)

    def _place(self, registry: SpawnRegistry, start_offscreen=False):
        w, h = self.rect.width, self.rect.height
        for _ in range(40):
            cx = random.choice(LANE_CX)
            y  = random.randint(-400, -h) if start_offscreen else -h
            r  = pygame.Rect(cx - w // 2, y, w, h)
            if registry.is_clear(r, margin=10):
                self.rect.centerx = cx
                self.rect.top     = y
                return
        # fallback — place far above screen
        self.rect.centerx = random.choice(LANE_CX)
        self.rect.top     = -600

    def get_rect(self): return self.rect

    def move(self, registry: SpawnRegistry):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_H:
            self._place(registry)

    def safe_reset(self, registry: SpawnRegistry):
        self._place(registry)


class Coin:
    def __init__(self, speed, registry: SpawnRegistry):
        self.radius = COIN_R
        self.speed  = speed
        self.active = True
        self._place(registry)

    def _place(self, registry: SpawnRegistry):
        pos = _safe_lane_place(registry, self.radius * 2, self.radius * 2, margin=6)
        if pos:
            self.x, self.y = pos[0], float(pos[1])
        else:
            self.x = random.choice(LANE_CX)
            self.y = float(-self.radius - random.randint(0, 200))
        self.value = random.choice(COIN_VALUES)
        self.color = COIN_COLORS[self.value]

    def move(self, registry: SpawnRegistry):
        self.y += self.speed
        if self.y - self.radius > SCREEN_H:
            self._place(registry)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE,      (self.x, int(self.y)), self.radius // 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)


class PowerUp:
    ICONS = {"nitro": "N", "shield": "S", "repair": "R"}

    def __init__(self, speed, registry: SpawnRegistry):
        self.radius  = PU_R
        self.speed   = speed
        self.kind    = random.choice(PU_TYPES)
        self.color   = PU_COLORS[self.kind]
        self.active  = True
        self.spawn_t = pygame.time.get_ticks()
        self._font   = pygame.font.SysFont("Verdana", 13, bold=True)
        pos = _safe_lane_place(registry, self.radius * 2, self.radius * 2, margin=8)
        if pos:
            self.x, self.y = pos[0], float(pos[1])
        else:
            self.x, self.y = random.choice(LANE_CX), float(-self.radius - 100)

    def move(self):
        self.y += self.speed
        if (self.y - self.radius > SCREEN_H
                or pygame.time.get_ticks() - self.spawn_t > PU_TIMEOUT):
            self.active = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color,  (self.x, int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE,        (self.x, int(self.y)), self.radius, 2)
        lbl = self._font.render(self.ICONS[self.kind], True, WHITE)
        surface.blit(lbl, (self.x - lbl.get_width()  // 2,
                           int(self.y) - lbl.get_height() // 2))

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def apply(self, player, obstacles):
        if self.kind == "nitro":
            player.activate_nitro()
            return "Nitro!"
        elif self.kind == "shield":
            player.shield = True
            return "Shield"
        elif self.kind == "repair":
            obstacles.clear()
            return "Repair!"
        return ""


# ── Lane obstacles ────────────────────────────────────────────────────────────

class LaneObstacle:
    def __init__(self, speed, registry: SpawnRegistry, w, h):
        self.speed  = speed
        self.active = True
        self.w, self.h = w, h
        pos = _safe_lane_place(registry, w, h, margin=10)
        if pos:
            self.cx, self.y = pos[0], float(pos[1])
        else:
            self.cx = random.choice(LANE_CX)
            self.y  = float(-h - random.randint(50, 300))

    def get_rect(self):
        return pygame.Rect(self.cx - self.w // 2, int(self.y), self.w, self.h)

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_H:
            self.active = False

    def is_lethal(self):   return True
    def apply_effect(self, player): pass


class OilSpill(LaneObstacle):
    def __init__(self, speed, registry):
        r = 18
        super().__init__(speed, registry, r * 2, r)
        self.r = r

    def draw(self, surface):
        x, y, r = self.cx, int(self.y), self.r
        pygame.draw.ellipse(surface, (15, 15, 50),  (x-r, y-r//2, r*2, r))
        pygame.draw.ellipse(surface, (70, 0, 110),  (x-r+4, y-r//2+2, r*2-8, r-4))

    def is_lethal(self):             return False
    def apply_effect(self, player):  player.activate_slow()


class Pothole(LaneObstacle):
    S = 28
    def __init__(self, speed, registry):
        super().__init__(speed, registry, self.S, self.S // 2)

    def draw(self, surface):
        x, y, s = self.cx, int(self.y), self.S
        pygame.draw.ellipse(surface, (30, 20, 20), (x-s//2, y, s, s//2))
        pygame.draw.ellipse(surface, (50, 35, 35), (x-s//2+4, y+3, s-8, s//2-6))


class Barrier(LaneObstacle):
    W, H = 60, 18
    def __init__(self, speed, registry):
        super().__init__(speed, registry, self.W, self.H)

    def draw(self, surface):
        x = self.cx - self.w // 2
        y = int(self.y)
        pygame.draw.rect(surface, ORANGE, (x, y, self.w, self.h))
        sw = self.w // 4
        for i in range(0, self.w, sw * 2):
            pygame.draw.rect(surface, WHITE, (x + i, y, sw, self.h))


class SpeedBump(LaneObstacle):
    def __init__(self, speed, registry):
        w = ROAD_RIGHT - ROAD_LEFT
        super().__init__(speed, registry, w, 10)
        self.cx = (ROAD_LEFT + ROAD_RIGHT) // 2

    def draw(self, surface):
        x, y = self.cx - self.w // 2, int(self.y)
        pygame.draw.rect(surface, (200, 180, 0), (x, y, self.w, self.h))
        sw = self.w // 8
        for i in range(0, self.w, sw * 2):
            pygame.draw.rect(surface, BLACK, (x + i, y, sw, self.h))

    def is_lethal(self):             return False
    def apply_effect(self, player):  player.activate_slow()


# ── Road-event strips ─────────────────────────────────────────────────────────

class NitroStrip:
    SIZE = 40
    def __init__(self, speed):
        self.speed  = speed
        self.w      = ROAD_RIGHT - ROAD_LEFT
        self.h      = self.SIZE
        self.x      = ROAD_LEFT
        self.y      = float(-self.h)
        self.active = True
        self._font  = pygame.font.SysFont("Verdana", 10, bold=True)

    def get_rect(self):
        return pygame.Rect(self.x, int(self.y), self.w, self.h)

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_H:
            self.active = False

    def draw(self, surface):
        x, y, w, h = self.x, int(self.y), self.w, self.h
        pygame.draw.rect(surface, (220, 160, 0), (x, y, w, h))
        pygame.draw.rect(surface, (255, 230, 80), (x, y, w, h), 2)
        for ax in range(x + 30, x + w - 10, 60):
            cx, cy, aw, ah = ax, y + h // 2, 14, 16
            pts = [(cx, cy-ah), (cx-aw, cy+ah//2), (cx-aw//2, cy+ah//2),
                   (cx-aw//2, cy+ah), (cx+aw//2, cy+ah),
                   (cx+aw//2, cy+ah//2), (cx+aw, cy+ah//2)]
            pygame.draw.polygon(surface, WHITE, pts)
        lbl = self._font.render("NITRO", True, (255, 80, 0))
        surface.blit(lbl, (x + 4, y + h // 2 - lbl.get_height() // 2))

    def apply(self, player):
        player.activate_nitro()
        return "Nitro Strip!"


class SlowStrip:
    SIZE = 40
    def __init__(self, speed):
        self.speed  = speed
        self.w      = ROAD_RIGHT - ROAD_LEFT
        self.h      = self.SIZE
        self.x      = ROAD_LEFT
        self.y      = float(-self.h)
        self.active = True
        self._font  = pygame.font.SysFont("Verdana", 10, bold=True)

    def get_rect(self):
        return pygame.Rect(self.x, int(self.y), self.w, self.h)

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_H:
            self.active = False

    def draw(self, surface):
        x, y, w, h = self.x, int(self.y), self.w, self.h
        pygame.draw.rect(surface, (30, 60, 140), (x, y, w, h))
        pygame.draw.rect(surface, (80, 140, 255), (x, y, w, h), 2)
        for ax in range(x + 30, x + w - 10, 60):
            cx, cy, aw, ah = ax, y + h // 2, 14, 16
            pts = [(cx, cy+ah), (cx-aw, cy-ah//2), (cx-aw//2, cy-ah//2),
                   (cx-aw//2, cy-ah), (cx+aw//2, cy-ah),
                   (cx+aw//2, cy-ah//2), (cx+aw, cy-ah//2)]
            pygame.draw.polygon(surface, WHITE, pts)
        lbl = self._font.render("SLOW", True, (180, 220, 255))
        surface.blit(lbl, (x + 4, y + h // 2 - lbl.get_height() // 2))

    def apply(self, player):
        player.activate_slow()
        return "Slowed!"


# ═════════════════════════════════════════════════════════════════════════════
#  Game loop
# ═════════════════════════════════════════════════════════════════════════════

def run_game(surface, clock, bg_image, player_images, enemy_image,
             crash_sound, settings, username, assets_dir: str = "assets") -> dict:
    """Run one session. Returns {score, distance, coins}."""

    mult     = DIFF_MULT.get(settings.get("difficulty", "normal"), 1.0)
    sound_on = settings.get("sound", True)
    color    = settings.get("car_color", "blue")

    registry = SpawnRegistry()

    player        = Player(player_images[color])
    enemy_grp     = pygame.sprite.Group()
    all_sprites   = pygame.sprite.Group(player)

    cur_speed = BASE_SPEED * mult

    def spawn_enemy():
        e = Enemy(enemy_image, cur_speed, registry)
        enemy_grp.add(e)
        all_sprites.add(e)

    spawn_enemy()

    coins: list[Coin]       = [Coin(cur_speed, registry)]
    obstacles: list         = []
    powerups: list[PowerUp] = []
    strips: list            = []   # NitroStrip / SlowStrip

    score = coin_count = distance = 0
    start_tick = pygame.time.get_ticks()
    road_y = 0

    now = pygame.time.get_ticks()
    next_obs   = now + int(3000  / mult)
    next_pu    = now + int(5000  / mult)
    next_strip = now + int(10000 / mult)

    active_label = ""

    if sound_on:
        try:
            pygame.mixer.music.load(os.path.join(assets_dir, "background.wav"))
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    running = True
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False   # back to menu without saving

        # ── Rebuild registry from ALL live objects this frame ─────────────
        live_objs = (list(enemy_grp) + coins + obstacles
                     + powerups + strips + [player])
        registry.rebuild(live_objs)

        # ── Difficulty scaling ─────────────────────────────────────────────
        tier      = coin_count // SPEED_UP_EVERY
        cur_speed = (BASE_SPEED + tier * SPEED_INC) * mult
        for c in coins:    c.speed = cur_speed
        for o in obstacles: o.speed = cur_speed
        for p in powerups:  p.speed = cur_speed
        for s in strips:    s.speed = cur_speed
        player.set_base_speed(BASE_SPEED + tier)

        for e in enemy_grp:
            e.speed = cur_speed

        desired = min(1 + coin_count // ENEMY_ADD_EVERY, MAX_ENEMIES)
        while len(enemy_grp) < desired:
            spawn_enemy()

        # ── Spawn obstacles ────────────────────────────────────────────────
        if now >= next_obs:
            kind = random.choices(
                ["oil", "pothole", "barrier", "bump"],
                weights=[3, 3, 2, 1]
            )[0]
            if kind == "oil":
                obstacles.append(OilSpill(cur_speed, registry))
            elif kind == "pothole":
                obstacles.append(Pothole(cur_speed, registry))
            elif kind == "barrier":
                obstacles.append(Barrier(cur_speed, registry))
            else:
                obstacles.append(SpeedBump(cur_speed, registry))
            next_obs = now + int(random.randint(1800, 3500) / mult)

        # ── Spawn power-up (max 1 on screen) ──────────────────────────────
        if now >= next_pu and not powerups:
            powerups.append(PowerUp(cur_speed, registry))
            next_pu = now + int(random.randint(6000, 10000) / mult)

        # ── Spawn road strip ───────────────────────────────────────────────
        if now >= next_strip and not strips:
            cls = random.choice([NitroStrip, SlowStrip])
            strips.append(cls(cur_speed))
            next_strip = now + int(random.randint(9000, 16000) / mult)

        # ── Move ──────────────────────────────────────────────────────────
        player.move()
        player.update_powerups()

        for e in enemy_grp:
            e.move(registry)

        # Add new coins to keep one always on screen
        for c in coins:
            c.move(registry)
        coins = [c for c in coins if c.active]
        if not coins:
            coins.append(Coin(cur_speed, registry))

        for o in obstacles: o.move()
        for p in powerups:  p.move()
        for s in strips:    s.move()

        obstacles = [o for o in obstacles if o.active]
        powerups  = [p for p in powerups  if p.active]
        strips    = [s for s in strips    if s.active]

        distance = (now - start_tick) // 100
        road_y   = (road_y + cur_speed) % SCREEN_H

        # ── Coin collision ─────────────────────────────────────────────────
        for c in coins[:]:
            if player.rect.colliderect(c.get_rect()):
                coin_count += 1
                score      += c.value
                coins.remove(c)
                coins.append(Coin(cur_speed, registry))

        # ── Power-up collision ─────────────────────────────────────────────
        for p in powerups[:]:
            if p.active and player.rect.colliderect(p.get_rect()):
                p.active = False
                active_label = p.apply(player, obstacles)
                score += 20

        # ── Strip collision ────────────────────────────────────────────────
        for s in strips[:]:
            if s.active and player.rect.colliderect(s.get_rect()):
                active_label = s.apply(player)
                s.active = False

        # ── Obstacle collision ─────────────────────────────────────────────
        for o in obstacles[:]:
            if player.rect.colliderect(o.get_rect()):
                if o.is_lethal():
                    if player.shield:
                        player.shield = False
                        active_label  = ""
                        o.active      = False
                    else:
                        running = False
                        break
                else:
                    o.apply_effect(player)
                    o.active = False
                    active_label = "Slowed!"

        # ── Enemy collision ────────────────────────────────────────────────
        if pygame.sprite.spritecollideany(player, enemy_grp):
            if player.shield:
                player.shield = False
                active_label  = ""
                for e in list(enemy_grp):
                    if player.rect.colliderect(e.rect):
                        e.safe_reset(registry)
            else:
                running = False

        # ── Clear stale labels ─────────────────────────────────────────────
        if active_label in ("Nitro!", "Nitro Strip!") and not player.nitro:
            active_label = ""
        if active_label == "Shield" and not player.shield:
            active_label = ""
        if active_label == "Slowed!" and not player.slowed:
            active_label = ""

        # ── Render ────────────────────────────────────────────────────────
        surface.blit(bg_image, (0, road_y - SCREEN_H))
        surface.blit(bg_image, (0, road_y))

        for s  in strips:    s.draw(surface)
        for o  in obstacles: o.draw(surface)
        for p  in powerups:  p.draw(surface)
        for c  in coins:     c.draw(surface)
        for sp in all_sprites:
            surface.blit(sp.image, sp.rect)

        # Shield bubble — pulsing cyan ring around the car
        if player.shield:
            pulse = abs((now // 8) % 40 - 20)          # 0-20 oscillation
            r_shield = player.rect.width // 2 + 8 + pulse // 4
            shield_surf = pygame.Surface(
                (r_shield * 2 + 4, r_shield * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (0, 220, 255, 80),
                               (r_shield + 2, r_shield + 2), r_shield)
            pygame.draw.circle(shield_surf, (0, 220, 255, 200),
                               (r_shield + 2, r_shield + 2), r_shield, 3)
            surface.blit(shield_surf,
                         (player.rect.centerx - r_shield - 2,
                          player.rect.centery - r_shield - 2))

        nitro_left = max(0, player.nitro_end - now) if player.nitro else 0
        draw_hud(surface, score, coin_count, distance,
                 player.shield, player.nitro, nitro_left, active_label)

        pygame.display.flip()
        clock.tick(FPS_CAP)

    # ── Crash sound ────────────────────────────────────────────────────────
    pygame.mixer.music.stop()
    if sound_on and crash_sound:
        try:
            crash_sound.play()
            pygame.time.wait(600)
        except Exception:
            pass

    return {"score": score, "distance": distance, "coins": coin_count}


# ═════════════════════════════════════════════════════════════════════════════
#  Screens
# ═════════════════════════════════════════════════════════════════════════════

def name_entry_screen(surface, clock, bg_image) -> str:
    cx  = SCREEN_W // 2
    inp = TextInput(cx - 120, 300, 240, 42, placeholder="Your name")
    btn = Button(cx - 80, 375, 160, 44, "Start →",
                 color=(40, 100, 40), hover_color=(60, 160, 60))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            inp.handle_event(event)
            if (btn.is_clicked(event)
                    or (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_RETURN)) \
                    and inp.text.strip():
                return inp.text.strip()

        draw_bg(surface, bg_image)
        draw_text(surface, "SPEED RACER", F_TITLE, YELLOW, cx, 160)
        draw_text(surface, "Enter your name", F_MED, WHITE, cx, 270)
        inp.draw(surface)
        btn.draw(surface)
        pygame.display.flip()
        clock.tick(FPS_CAP)


def main_menu(surface, clock, bg_image) -> str:
    cx = SCREEN_W // 2
    buttons = {
        "play":        Button(cx - 90, 220, 180, 46, "▶  Play"),
        "leaderboard": Button(cx - 90, 278, 180, 46, "🏆  Leaderboard"),
        "settings":    Button(cx - 90, 336, 180, 46, "⚙  Settings"),
        "quit":        Button(cx - 90, 394, 180, 46, "✕  Quit",
                              color=(100, 30, 30), hover_color=(160, 50, 50)),
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for key, btn in buttons.items():
                if btn.is_clicked(event):
                    return key

        draw_bg(surface, bg_image)
        draw_text(surface, "SPEED RACER", F_TITLE, YELLOW, cx, 140)
        draw_text(surface, "v2.0", F_TINY, GRAY, cx, 185)
        for btn in buttons.values():
            btn.draw(surface)
        pygame.display.flip()
        clock.tick(FPS_CAP)


# ── Settings screen ───────────────────────────────────────────────────────────

_CAR_RGB = {
    "blue":   (50,  120, 255),
    "red":    (220, 50,  50),
    "green":  (50,  200, 70),
    "yellow": (255, 210, 0),
}
_DIFF_RGB = {"easy": GREEN, "normal": YELLOW, "hard": RED}
_SWATCH   = 40
_SWATCH_G = 8


def settings_screen(surface, clock, bg_image, settings: dict, save_fn):
    from persistence import save_settings as _save
    cx = SCREEN_W // 2

    PANEL_W   = 360
    panel_x   = cx - PANEL_W // 2
    TOGGLE_H  = 48

    sound_rect = pygame.Rect(panel_x, 130, PANEL_W, TOGGLE_H)
    diff_rect  = pygame.Rect(panel_x, 192, PANEL_W, TOGGLE_H)
    btn_save   = Button(cx - 90, SCREEN_H - 76, 180, 46, "Save & Back",
                        color=(40, 100, 40), hover_color=(60, 160, 60))

    diff_opts = ["easy", "normal", "hard"]

    # colour swatches
    n_sw      = len(CAR_COLORS)
    total_sw  = n_sw * _SWATCH + (n_sw - 1) * _SWATCH_G
    sw_x0     = cx - total_sw // 2
    SW_Y      = 295
    SW_LABEL_Y = SW_Y + _SWATCH + 6

    def _swatch_rect(i):
        return pygame.Rect(sw_x0 + i * (_SWATCH + _SWATCH_G), SW_Y, _SWATCH, _SWATCH)

    def _draw_toggle_row(label, value_text, value_color, rect):
        pygame.draw.rect(surface, (25, 25, 35), rect, border_radius=8)
        pygame.draw.rect(surface, (60, 60, 80), rect, 1, border_radius=8)
        lbl = F_MED.render(label, True, WHITE)
        surface.blit(lbl, (rect.x + 14, rect.centery - lbl.get_height() // 2))
        pill = pygame.Rect(rect.right - 100, rect.centery - 14, 88, 28)
        pygame.draw.rect(surface, (40, 40, 60), pill, border_radius=14)
        pygame.draw.rect(surface, value_color, pill, 2, border_radius=14)
        vl = F_SMALL.render(value_text, True, value_color)
        surface.blit(vl, vl.get_rect(center=pill.center))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if sound_rect.collidepoint(pos):
                    settings["sound"] = not settings["sound"]
                elif diff_rect.collidepoint(pos):
                    idx = diff_opts.index(settings["difficulty"])
                    settings["difficulty"] = diff_opts[(idx + 1) % 3]
                elif btn_save.is_clicked(event):
                    save_fn(settings)
                    return
                else:
                    for i, col in enumerate(CAR_COLORS):
                        if _swatch_rect(i).collidepoint(pos):
                            settings["car_color"] = col

        draw_bg(surface, bg_image)
        draw_text(surface, "Settings", F_LARGE, YELLOW, cx, 68)
        pygame.draw.line(surface, (60, 60, 80), (panel_x, 98), (panel_x + PANEL_W, 98))

        # Sound toggle
        s_lbl = "ON" if settings["sound"] else "OFF"
        s_col = GREEN if settings["sound"] else RED
        _draw_toggle_row("Sound", s_lbl, s_col, sound_rect)

        # Difficulty toggle
        d = settings["difficulty"]
        _draw_toggle_row("Difficulty", d.capitalize(), _DIFF_RGB[d], diff_rect)

        # Car colour header
        draw_text(surface, "Car colour", F_MED, GRAY, cx, 272)

        # Swatches
        for i, col in enumerate(CAR_COLORS):
            sr  = _swatch_rect(i)
            rgb = _CAR_RGB[col]
            sel = settings["car_color"] == col
            if sel:
                pygame.draw.rect(surface, rgb, sr.inflate(8, 8), border_radius=10)
            pygame.draw.rect(surface, rgb, sr, border_radius=7)
            pygame.draw.rect(surface, WHITE if sel else (70, 70, 70), sr, 2, border_radius=7)
            lbl = F_TINY.render(col.capitalize(), True, WHITE if sel else GRAY)
            surface.blit(lbl, lbl.get_rect(centerx=sr.centerx, top=SW_LABEL_Y))

        # Mini car preview
        draw_text(surface, "Preview", F_TINY, GRAY, cx, SW_LABEL_Y + 22)

        btn_save.draw(surface)
        draw_text(surface, "ESC — back without saving", F_TINY, (70, 70, 70), cx, SCREEN_H - 18)

        pygame.display.flip()
        clock.tick(FPS_CAP)


def leaderboard_screen(surface, clock, bg_image):
    from persistence import load_leaderboard
    cx       = SCREEN_W // 2
    btn_back = Button(cx - 70, SCREEN_H - 54, 140, 38, "← Back")
    entries  = load_leaderboard()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if btn_back.is_clicked(event) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

        draw_bg(surface, bg_image)
        draw_text(surface, "Leaderboard", F_LARGE, YELLOW, cx, 52)

        # header row
        cols = [30, 120, 240, 340]
        hdrs = ["#", "Name", "Score", "Dist m"]
        for hx, ht in zip(cols, hdrs):
            draw_text(surface, ht, F_TINY, GRAY, hx, 94)
        pygame.draw.line(surface, GRAY, (10, 108), (390, 108), 1)

        for i, e in enumerate(entries[:10]):
            y   = 126 + i * 38
            col = YELLOW if i == 0 else WHITE
            for hx, val in zip(cols, [str(i+1), e.get("name","?"),
                                       str(e.get("score",0)),
                                       str(e.get("distance",0))]):
                draw_text(surface, val, F_SMALL, col, hx, y)

        if not entries:
            draw_text(surface, "No scores yet!", F_MED, GRAY, cx, 300)

        btn_back.draw(surface)
        pygame.display.flip()
        clock.tick(FPS_CAP)


def game_over_screen(surface, clock, bg_image, score, distance, coins) -> str:
    cx        = SCREEN_W // 2
    btn_retry = Button(cx - 100, 420, 180, 46, "▶ Retry")
    btn_menu  = Button(cx - 100, 478, 180, 46, "⌂ Main Menu",
                       color=(60, 30, 80), hover_color=(100, 50, 130))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if btn_retry.is_clicked(event): return "retry"
            if btn_menu.is_clicked(event):  return "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:      return "retry"
                if event.key == pygame.K_ESCAPE: return "menu"

        draw_bg(surface, bg_image)
        draw_text(surface, "GAME OVER",       F_TITLE, RED,    cx, 140)
        draw_text(surface, f"Score:    {score}",     F_MED,  WHITE,  cx, 240)
        draw_text(surface, f"Distance: {distance}m", F_MED,  WHITE,  cx, 275)
        draw_text(surface, f"Coins:    {coins}",     F_MED,  YELLOW, cx, 310)
        btn_retry.draw(surface)
        btn_menu.draw(surface)
        pygame.display.flip()
        clock.tick(FPS_CAP)