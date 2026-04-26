import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

#some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (100, 200, 255)

#movement
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)


#about snake
class Snake:
    def __init__(self):
        self.positions = [
            [GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
            [GRID_WIDTH // 2 * GRID_SIZE - GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
            [GRID_WIDTH // 2 * GRID_SIZE - 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE]
        ]
        self.direction = RIGHT
        self.grow_flag = False
        self.color = GREEN
        self.head_color = (0, 200, 0)

    def move(self):
        head = self.positions[0].copy()
        head[0] += self.direction[0] * GRID_SIZE
        head[1] += self.direction[1] * GRID_SIZE
        
        self.positions.insert(0, head)
        
        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False

    def change_direction(self, new_direction):
        if (new_direction[0] != -self.direction[0] or 
            new_direction[1] != -self.direction[1]):
            self.direction = new_direction

    def grow(self):
        self.grow_flag = True

    def check_self_collision(self):
        head = self.positions[0]
        return head in self.positions[1:]

    def check_border_collision(self):
        head = self.positions[0]
        return (head[0] < 0 or head[0] >= SCREEN_WIDTH or
                head[1] < 0 or head[1] >= SCREEN_HEIGHT)

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            if i == 0:
                pygame.draw.rect(surface, self.head_color, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, WHITE, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE), 2)
            else:
                pygame.draw.rect(surface, self.color, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, BLACK, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE), 1)

    def check_wall_collision(self, walls):
        return self.positions[0] in walls.positions

#about food
class Food:
    def __init__(self, snake_positions, walls_positions=[]):
        self.position = [0, 0]
        self.color = RED
        self.walls_positions = walls_positions
        self.spawn_time = pygame.time.get_ticks()
        self.respawn(snake_positions, walls_positions)

    def respawn(self, snake_positions, walls_positions=[]):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            if [x, y] not in snake_positions and [x, y] not in walls_positions:
                self.position = [x, y]
                self.spawn_time = pygame.time.get_ticks()
                break
    
    def update(self):
        current_time = pygame.time.get_ticks()
        time_alive = current_time - self.spawn_time

        # if 45 seconds passed → force respawn
        if time_alive > 45000:
            return "RESPAWN"

        return time_alive

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, 
                        (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, WHITE, 
                        (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE), 2)

#about border and labyrint 
class Walls:
    def __init__(self):
        self.positions = []

    def generate(self, level):
        if level < 2:
            return

        
        if level % 2 == 0:
            base_x = random.randint(3, GRID_WIDTH - 8) * GRID_SIZE
            base_y = random.randint(3, GRID_HEIGHT - 8) * GRID_SIZE

            shape_type = random.choice([0, 1, 2, 3])
            new_blocks = []

            if shape_type == 0:  
                for i in range(5):
                    new_blocks.append([base_x, base_y + i * GRID_SIZE])
                for i in range(5):
                    new_blocks.append([base_x + i * GRID_SIZE, base_y])

            elif shape_type == 1:  
                for i in range(5):
                    new_blocks.append([base_x, base_y + i * GRID_SIZE])
                for i in range(5):
                    new_blocks.append([base_x - i * GRID_SIZE, base_y])

            elif shape_type == 2:  
                for i in range(5):
                    new_blocks.append([base_x, base_y - i * GRID_SIZE])
                for i in range(5):
                    new_blocks.append([base_x + i * GRID_SIZE, base_y])

            else:  
                for i in range(5):
                    new_blocks.append([base_x, base_y - i * GRID_SIZE])
                for i in range(5):
                    new_blocks.append([base_x - i * GRID_SIZE, base_y])

            for block in new_blocks:
                if block not in self.positions:
                    self.positions.append(block)

        
        else:
            for _ in range(3):  
                x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
                y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

                if [x, y] not in self.positions:
                    self.positions.append([x, y])



    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, LIGHT_BLUE,
                             (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE,
                             (pos[0], pos[1], GRID_SIZE, GRID_SIZE), 1)

def show_game_over(screen, score, level):
    screen.fill(BLACK)
    
    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    level_text = font.render(f"Level Reached: {level}", True, YELLOW)
    restart_text = font.render("Press SPACE to restart", True, GREEN)
    quit_text = font.render("Press ESC to quit", True, GREEN)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 150))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
    screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 300))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 400))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 450))
    
    pygame.display.flip()

def main():
    snake = Snake()
    food = Food(snake.positions)
    
    score = 0
    level = 1
    walls = Walls()
    walls.generate(level)
    foods_eaten = 0
    FOODS_PER_LEVEL = 3
    
    base_speed = 10
    current_speed = base_speed
    
    running = True
    game_active = True
    
    while running:
        clock.tick(current_speed)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_active:
                    # Arrow keys + WASD controls
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    # Key F to fix problem with stacked food
                    elif event.key == pygame.K_f:
                        food.respawn(snake.positions, walls.positions)


                else:
                    if event.key == pygame.K_SPACE:
                        score = 0
                        level = 1
                        foods_eaten = 0
                        current_speed = base_speed

                        snake = Snake()
                        food = Food(snake.positions)

                        walls = Walls()
                        walls.generate(level)

                        game_active = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        if game_active:
            snake.move()

            result = food.update()
            if result == "RESPAWN":
                food.respawn(snake.positions, walls.positions)
            
            if (snake.check_border_collision() or snake.check_self_collision() or snake.check_wall_collision(walls)):
                game_active = False
                continue
            
            if snake.positions[0] == food.position:
                snake.grow()
                score += 10
                foods_eaten += 1
                
                if foods_eaten >= FOODS_PER_LEVEL:
                    level += 1
                    foods_eaten = 0
                    current_speed = base_speed + (level * 2)

                    walls.generate(level)   
                
                food.respawn(snake.positions)
            
            screen.fill(BLACK)
            
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))
            
            walls.draw(screen)
            snake.draw(screen)
            food.draw(screen)
            
            score_text = font.render(f"Score: {score}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, YELLOW)
            speed_text = font.render(f"Speed: {current_speed}", True, CYAN)
            
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))
            screen.blit(speed_text, (10, 90))
            
            foods_left_text = font.render(f"Next Level: {foods_eaten}/{FOODS_PER_LEVEL}", True, PURPLE)
            screen.blit(foods_left_text, (10, 130))
            
            
            
        else:
            show_game_over(screen, score, level)
        



        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()