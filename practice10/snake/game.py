import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Font for UI (score, level, game over)
font = pygame.font.SysFont("Verdana", 20)

# ---------- GRID ----------
def draw_grid():
    # Draws grid lines across the screen
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

# ---------- POINT ----------
class Point:
    # Simple class to store x and y coordinates
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ---------- SNAKE ----------
class Snake:
    def __init__(self):
        # Initial snake body (3 segments)
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1  # horizontal direction
        self.dy = 0  # vertical direction

    def move(self):
        # Move body: each segment follows the previous one
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # Move head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def check_wall_collision(self):
        # Returns True if snake hits the wall
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        return False

    def draw(self):
        # Draw head
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        # Draw body
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        # Check if snake eats food
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            # Grow snake
            self.body.append(Point(head.x, head.y))
            return True
        return False
    
    def check_self_collision(self):
        head = self.body[0]

        # check collision with body (skip head)
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False
# ---------- FOOD ----------
class Food:
    def __init__(self):
        self.pos = Point(5, 5)

    def draw(self):
        # Draw food as a green square
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake):
        # Generate position that does NOT overlap with snake
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            collision = False
            for segment in snake.body:
                if segment.x == x and segment.y == y:
                    collision = True
                    break

            if not collision:
                self.pos.x = x
                self.pos.y = y
                break

# ---------- GAME SETTINGS ----------
score = 0
level = 1
FPS = 5
clock = pygame.time.Clock()

food = Food()
snake = Snake()

running = True
game_over = False

def reset_game():
    global snake, food, score, level, FPS, game_over

    snake = Snake()
    food = Food()
    food.generate_random_pos(snake)

    score = 0
    level = 1
    FPS = 5
    game_over = False

# ---------- GAME LOOP ----------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle movement input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP:
                snake.dx, snake.dy = 0, -1
        #Reset game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        snake.move()

    # wall collision
    if snake.check_wall_collision():
        game_over = True

    # self collision
    if snake.check_self_collision():
        game_over = True

    # food collision
    if snake.check_collision(food):
        score += 1
        food.generate_random_pos(snake)

        if score % 4 == 0:
            level += 1
            FPS += 1
    # ---------- DRAW ----------
    screen.fill(colorBLACK)
    draw_grid()

    snake.draw()
    food.draw()

    # Render score and level text
    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    # Show game over message
    if game_over:
        over_text = font.render("GAME OVER", True, colorRED)
        restart_text = font.render("Press R to restart", True, colorWHITE)

        screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()