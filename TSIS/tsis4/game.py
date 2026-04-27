"""
game.py — game entities: Snake, Food, PoisonFood, PowerUp, Obstacle
"""

import pygame
import random

from color_palette import *
from config import (
    CELL, PLAY_COLS, PLAY_ROWS,
    POISON_CHANCE, POWERUP_FIELD_LIFETIME, POWERUP_DURATION,
    SPEED_BOOST_DELTA, POWERUP_TYPES,
    OBSTACLE_START_LEVEL, OBSTACLES_PER_LEVEL,
)


# ═══════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════

class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def _free_cell(occupied: list["Point"]) -> tuple[int, int]:
    """Pick a random grid cell not occupied by the given points."""
    occupied_set = {(p.x, p.y) for p in occupied}
    while True:
        x = random.randint(0, PLAY_COLS - 1)
        y = random.randint(0, PLAY_ROWS - 1)
        if (x, y) not in occupied_set:
            return x, y


# ═══════════════════════════════════════════════
#  Snake
# ═══════════════════════════════════════════════

class Snake:
    def __init__(self, color: tuple = colorGREEN):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.color = color
        self.pending_grow = False

        # Power-up state
        self.shield_active = False        # absorbs one lethal collision
        self.speed_effect = 0             # +delta applied to base FPS
        self.effect_end_time = 0          # when current timed effect expires

    # --- direction ---
    def change_direction(self, dx: int, dy: int) -> None:
        if self.dx == -dx and self.dy == -dy:
            return
        self.dx = dx
        self.dy = dy

    # --- movement ---
    def move(self) -> None:
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def grow(self) -> None:
        tail = self.body[-1]
        self.body.append(Point(tail.x, tail.y))

    def shrink(self, n: int = 2) -> bool:
        """Remove n tail segments. Returns True if snake is dead (len <= 1)."""
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()
        return len(self.body) <= 1

    # --- collisions ---
    def head(self) -> Point:
        return self.body[0]

    def check_wall_collision(self) -> bool:
        h = self.head()
        return h.x < 0 or h.x >= PLAY_COLS or h.y < 0 or h.y >= PLAY_ROWS

    def check_self_collision(self) -> bool:
        h = self.head()
        return any(h.x == s.x and h.y == s.y for s in self.body[1:])

    def check_obstacle_collision(self, obstacles: list["Obstacle"]) -> bool:
        h = self.head()
        return any(h.x == o.pos.x and h.y == o.pos.y for o in obstacles)

    # --- power-up timing ---
    def tick_effects(self) -> int:
        """Return current speed delta (0 if no timed effect active)."""
        if self.speed_effect != 0:
            if pygame.time.get_ticks() >= self.effect_end_time:
                self.speed_effect = 0
        return self.speed_effect

    def apply_speed_effect(self, delta: int) -> None:
        self.speed_effect = delta
        self.effect_end_time = pygame.time.get_ticks() + POWERUP_DURATION

    # --- drawing ---
    def draw(self, surface: pygame.Surface) -> None:
        head_color = colorRED if not self.shield_active else colorCYAN
        pygame.draw.rect(
            surface, head_color,
            (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL),
        )
        for seg in self.body[1:]:
            pygame.draw.rect(
                surface, self.color,
                (seg.x * CELL, seg.y * CELL, CELL, CELL),
            )


# ═══════════════════════════════════════════════
#  Food
# ═══════════════════════════════════════════════

class Food:
    def __init__(self):
        self.pos = Point(0, 0)
        self.value = 1
        self.color = colorGREEN
        self.lifetime = 7000
        self.spawn_time = pygame.time.get_ticks()

    def place(self, occupied: list[Point]) -> None:
        x, y = _free_cell(occupied)
        self.pos.x, self.pos.y = x, y
        self._randomise()

    def _randomise(self) -> None:
        self.value = random.choice([1, 2, 3])
        if self.value == 1:
            self.color = colorGREEN
            self.lifetime = 7000
        elif self.value == 2:
            self.color = colorYELLOW
            self.lifetime = 5500
        else:
            self.color = colorORANGE
            self.lifetime = 3500
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface, self.color,
            (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL),
        )
        # small dot to distinguish from snake body
        pygame.draw.circle(
            surface, colorWHITE,
            (self.pos.x * CELL + CELL // 2, self.pos.y * CELL + CELL // 2),
            CELL // 5,
        )


class PoisonFood(Food):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.color = colorDARK_RED
        self.lifetime = 6000

    def _randomise(self) -> None:
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface, self.color,
            (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL),
        )
        # skull-like X marker
        x0, y0 = self.pos.x * CELL + 4, self.pos.y * CELL + 4
        x1, y1 = self.pos.x * CELL + CELL - 4, self.pos.y * CELL + CELL - 4
        pygame.draw.line(surface, colorWHITE, (x0, y0), (x1, y1), 2)
        pygame.draw.line(surface, colorWHITE, (x1, y0), (x0, y1), 2)


# ═══════════════════════════════════════════════
#  Power-up
# ═══════════════════════════════════════════════

_POWERUP_META = {
    "speed":  {"color": colorCYAN,   "label": "⚡"},
    "slow":   {"color": colorPURPLE, "label": "🐢"},
    "shield": {"color": colorLIGHT_BLUE, "label": "🛡"},
}


class PowerUp:
    def __init__(self, kind: str):
        self.kind = kind
        self.pos = Point(0, 0)
        self.spawn_time = pygame.time.get_ticks()
        self.color = _POWERUP_META[kind]["color"]
        self.label = _POWERUP_META[kind]["label"]

    def place(self, occupied: list[Point]) -> None:
        x, y = _free_cell(occupied)
        self.pos.x, self.pos.y = x, y

    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.spawn_time > POWERUP_FIELD_LIFETIME

    def apply(self, snake: Snake, game_state: dict) -> None:
        if self.kind == "speed":
            snake.apply_speed_effect(+SPEED_BOOST_DELTA)
        elif self.kind == "slow":
            snake.apply_speed_effect(-SPEED_BOOST_DELTA)
        elif self.kind == "shield":
            snake.shield_active = True

    def draw(self, surface: pygame.Surface) -> None:
        r = pygame.Rect(self.pos.x * CELL, self.pos.y * CELL, CELL, CELL)
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        pygame.draw.rect(surface, colorWHITE, r, 2, border_radius=6)


# ═══════════════════════════════════════════════
#  Obstacle
# ═══════════════════════════════════════════════

class Obstacle:
    def __init__(self, x: int, y: int):
        self.pos = Point(x, y)

    def draw(self, surface: pygame.Surface) -> None:
        r = pygame.Rect(self.pos.x * CELL, self.pos.y * CELL, CELL, CELL)
        pygame.draw.rect(surface, colorDARK_GRAY, r)
        pygame.draw.rect(surface, colorGRAY, r, 2)


def generate_obstacles(level: int, snake: Snake, existing: list[Obstacle]) -> list[Obstacle]:
    """
    Create fresh obstacles for the given level.
    Number of obstacles = OBSTACLES_PER_LEVEL * (level - OBSTACLE_START_LEVEL + 1).
    Guarantees none overlap snake body.
    """
    if level < OBSTACLE_START_LEVEL:
        return []

    count = OBSTACLES_PER_LEVEL * (level - OBSTACLE_START_LEVEL + 1)
    occupied = list(snake.body)
    obstacles: list[Obstacle] = []
    occ_set = {(p.x, p.y) for p in snake.body}

    for _ in range(count):
        while True:
            x = random.randint(0, PLAY_COLS - 1)
            y = random.randint(0, PLAY_ROWS - 1)
            if (x, y) not in occ_set:
                obstacles.append(Obstacle(x, y))
                occ_set.add((x, y))
                break

    return obstacles


# ═══════════════════════════════════════════════
#  Food / PowerUp factory
# ═══════════════════════════════════════════════

def spawn_food(snake: Snake, obstacles: list[Obstacle]) -> Food:
    occupied = snake.body + [o.pos for o in obstacles]
    if random.random() < POISON_CHANCE:
        f = PoisonFood()
    else:
        f = Food()
    f.place(occupied)
    return f


def spawn_powerup(snake: Snake, obstacles: list[Obstacle], foods: list[Food]) -> PowerUp:
    kind = random.choice(POWERUP_TYPES)
    pu = PowerUp(kind)
    occupied = snake.body + [o.pos for o in obstacles] + [f.pos for f in foods]
    pu.place(occupied)
    return pu