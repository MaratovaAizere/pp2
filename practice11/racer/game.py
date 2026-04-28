# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initialize pygame
pygame.init()

# FPS setup
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0          # total score (depends on coin value)
COIN_COUNT = 0     # number of collected coins

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("AnimatedStreet.png")

# Create game window
DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Game")


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        # Move enemy downward
        self.rect.move_ip(0, SPEED)

        # Reset position if it goes off screen
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # Move left
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        # Move right
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Coin class (color represents value)
class Coin:
    def __init__(self, x, y, radius=15, speed=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.set_random_value()

    def set_random_value(self):
        # Assign random value and corresponding color
        choice = random.choice([1, 5, 10])
        self.value = choice

        if choice == 1:
            self.color = (255, 215, 0)   # yellow (low value)
        elif choice == 5:
            self.color = (0, 255, 0)     # green (medium value)
        else:
            self.color = (255, 0, 0)     # red (high value)

    def move(self):
        # Move coin downward
        self.y += self.speed

        # Reset if off screen
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(20, SCREEN_WIDTH - 20)
            self.set_random_value()

    def draw(self, surface):
        # Draw coin as a circle
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def get_rect(self):
        # Return rectangle for collision detection
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)


# Generate safe coin position (avoid spawning on enemy)
def get_safe_coin_position(enemy, radius):
    while True:
        x = random.randint(radius, SCREEN_WIDTH - radius)
        y = 0

        coin_rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)

        if not coin_rect.colliderect(enemy.rect):
            return x, y


# Create game objects
P1 = Player()
E1 = Enemy()

# Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Create coin
x, y = get_safe_coin_position(E1, 15)
coin = Coin(x, y)


# Main game loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Display UI (score and coins)
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COIN_COUNT}", True, BLACK)

    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (10, 30))

    # Update coin
    coin.move()
    coin.draw(DISPLAYSURF)

    # Move and draw all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check coin collision
    if P1.rect.colliderect(coin.get_rect()):
        COIN_COUNT += 1
        SCORE += coin.value

        # Increase enemy speed every 5 coins
        if COIN_COUNT % 5 == 0:
            SPEED += 1

        coin.x, coin.y = get_safe_coin_position(E1, coin.radius)
        coin.set_random_value()

    # Check collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()

        # Remove all sprites
        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)