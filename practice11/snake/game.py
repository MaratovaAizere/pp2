import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Font
font = pygame.font.SysFont("Verdana", 20)

# ---------- GRID ----------
def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

# ---------- POINT ----------
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ---------- SNAKE ----------
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def change_direction(self, dx, dy):
        # Prevent 180-degree turn
        if self.dx == -dx and self.dy == -dy:
            return
        self.dx = dx
        self.dy = dy

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def check_wall_collision(self):
        head = self.body[0]
        return head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL

    def check_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            return True
        return False

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

# ---------- FOOD ----------
class Food:
    def __init__(self):
        self.pos = Point(0, 0)
        self.spawn_time = pygame.time.get_ticks()
        self.set_random_properties()

    def set_random_properties(self):
        # Random value + lifetime
        self.value = random.choice([1, 2, 3])

        if self.value == 1:
            self.color = colorGREEN
            self.lifetime = 7000
        elif self.value == 2:
            self.color = colorYELLOW
            self.lifetime = 5500
        else:
            self.color = colorRED
            self.lifetime = 3500

        self.spawn_time = pygame.time.get_ticks()

    def generate_random_pos(self, snake):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            if all(segment.x != x or segment.y != y for segment in snake.body):
                self.pos.x = x
                self.pos.y = y
                self.set_random_properties()
                break

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

# ---------- GAME ----------
score = 0
level = 1
FPS = 5
clock = pygame.time.Clock()

snake = Snake()
foods = []

# Spawn event
SPAWN_FOOD_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_FOOD_EVENT, 2000)

running = True
game_over = False

def reset_game():
    global snake, foods, score, level, FPS, game_over
    snake = Snake()
    foods = []
    score = 0
    level = 1
    FPS = 5
    game_over = False

# ---------- LOOP ----------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_FOOD_EVENT:
            new_food = Food()
            new_food.generate_random_pos(snake)
            foods.append(new_food)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_direction(1, 0)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(-1, 0)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(0, 1)
            elif event.key == pygame.K_UP:
                snake.change_direction(0, -1)

            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        snake.move()

    # Collisions
    if snake.check_wall_collision() or snake.check_self_collision():
        game_over = True

    # Food logic
    for food in foods[:]:
        if snake.check_collision(food):
            score += food.value
            foods.remove(food)

            if score % 4 == 0:
                level += 1
                FPS += 1

        elif food.is_expired():
            foods.remove(food)

    # ---------- DRAW ----------
    screen.fill(colorBLACK)
    draw_grid()

    snake.draw()

    for food in foods:
        food.draw()

    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    if game_over:
        over_text = font.render("GAME OVER", True, colorRED)
        restart_text = font.render("Press R to restart", True, colorWHITE)

        screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()