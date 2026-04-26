# Imports
import pygame
import sys
from pygame.locals import *
import random
import time

# Initialize Pygame
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 30)

# Game Over text
game_over = font.render("Game Over", True, BLACK)

# Function to load images with error handling
def load_image(filename, default_color=None, width=None, height=None):
    """Load image from images folder or create colored placeholder"""
    try:
        # Try loading from images folder first
        import os
        path = os.path.join("images", filename)
        if os.path.exists(path):
            image = pygame.image.load(path)
        else:
            image = pygame.image.load(filename)
        
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
    except:
        print(f"Warning: Could not load {filename}, creating placeholder")
        if default_color:
            size = (width or 50, height or 50)
            image = pygame.Surface(size)
            image.fill(default_color)
            return image
        return None

# Load images
background = load_image("AnimatedStreet.png", GRAY, SCREEN_WIDTH, SCREEN_HEIGHT)
player_img = load_image("Player.png", BLUE, 50, 80)
enemy_img = load_image("Enemy.png", RED, 50, 80)
coin_img = load_image("coin.png", YELLOW, 30, 30)  # Using coin.png as requested

# Create display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Racer")
DISPLAYSURF.fill(WHITE)

class Player(pygame.sprite.Sprite):
    """Player car class"""
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        self.speed = 7

    def move(self):
        """Handle player movement"""
        pressed_keys = pygame.key.get_pressed()
        
        # Move left (Left arrow or A key)
        if (pressed_keys[K_LEFT] or pressed_keys[K_a]) and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        
        # Move right (Right arrow or D key)
        if (pressed_keys[K_RIGHT] or pressed_keys[K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(self.speed, 0)

    def draw(self, surface):
        """Draw player on screen"""
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    """Enemy car class"""
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        """Reset enemy to top of screen"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Move enemy down the screen"""
        global SCORE
        self.rect.move_ip(0, SPEED)
        
        # If enemy goes off screen, reset and increase score
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset_position()

    def draw(self, surface):
        """Draw enemy on screen"""
        surface.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    """Coin class - appears rarely"""
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset_position()
        self.spawn_delay = random.randint(60, 180)  # Delay before appearing
        self.active = False
        self.delay_counter = 0

    def reset_position(self):
        """Reset coin to random position at top"""
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 30),
            random.randint(-500, -100)  # Start higher up for rarity
        )
        self.active = True

    def move(self):
        """Move coin down the screen"""
        if not self.active:
            self.delay_counter += 1
            if self.delay_counter >= self.spawn_delay:
                self.active = True
                self.delay_counter = 0
                self.spawn_delay = random.randint(120, 300)  # Long delay between spawns
            return
        
        self.rect.move_ip(0, SPEED // 2)  # Coins fall slower
        
        # Reset if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.active = False
            self.reset_position()

    def draw(self, surface):
        """Draw coin on screen if active"""
        if self.active:
            surface.blit(self.image, self.rect)

def show_game_over(score, coins):
    """Display game over screen"""
    DISPLAYSURF.fill(RED)
    
    # Create text surfaces
    game_over_text = font.render("GAME OVER", True, BLACK)
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    coins_text = font_medium.render(f"Coins: {coins}", True, YELLOW)
    restart_text = font_small.render("Press SPACE to restart", True, GREEN)
    quit_text = font_small.render("Press ESC to quit", True, GREEN)
    
    # Display texts
    DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 150))
    DISPLAYSURF.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH//2 - coins_text.get_width()//2, 290))
    DISPLAYSURF.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 400))
    DISPLAYSURF.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 440))
    
    pygame.display.update()

def reset_game():
    """Reset all game variables"""
    global SCORE, COINS_COLLECTED, SPEED
    SCORE = 0
    COINS_COLLECTED = 0
    SPEED = 5
    
    # Reset sprites
    P1.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
    E1.reset_position()
    
    # Reset coins
    for coin in coins:
        coin.active = False
        coin.delay_counter = 0
        coin.spawn_delay = random.randint(120, 300)

# Initialize game objects
P1 = Player()
E1 = Enemy()

# Create sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
# Create only 1 coin for rarity
coin1 = Coin()
coins.add(coin1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin1)

# Custom event for gradual speed increase (smooth, no sharp screen)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 5000)  # Increase speed every 5 seconds (smooth)

# Game states
PLAYING = 0
GAME_OVER = 1
game_state = PLAYING

# Background scrolling variables
bg_y = 0
bg_scroll_speed = 2

# Main game loop
while True:
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if game_state == PLAYING:
            if event.type == INC_SPEED:
                SPEED += 0.2  # Very gradual speed increase (smooth)
                if SPEED > 10:  # Cap the speed
                    SPEED = 10
        
        elif game_state == GAME_OVER:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    reset_game()
                    game_state = PLAYING
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    if game_state == PLAYING:
        # Scroll background smoothly
        bg_y = (bg_y + bg_scroll_speed) % SCREEN_HEIGHT
        DISPLAYSURF.blit(background, (0, bg_y - SCREEN_HEIGHT))
        DISPLAYSURF.blit(background, (0, bg_y))
        
        # Move all sprites
        P1.move()
        E1.move()
        for coin in coins:
            coin.move()
        
        # Check coin collisions (only if coin is active)
        for coin in coins:
            if coin.active and P1.rect.colliderect(coin.rect):
                COINS_COLLECTED += 1
                SCORE += 10  # Bonus points for coin
                coin.active = False
                coin.reset_position()
        
        # Check enemy collision
        if P1.rect.colliderect(E1.rect):
            time.sleep(0.5)  # Brief pause before game over
            game_state = GAME_OVER
        
        # Draw all sprites
        DISPLAYSURF.blit(background, (0, bg_y - SCREEN_HEIGHT))
        DISPLAYSURF.blit(background, (0, bg_y))
        
        P1.draw(DISPLAYSURF)
        E1.draw(DISPLAYSURF)
        for coin in coins:
            coin.draw(DISPLAYSURF)
        
        # Draw UI elements
        score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
        coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
        speed_text = font_small.render(f"Speed: {SPEED:.1f}", True, RED if SPEED > 7 else BLACK)
        
        # White background for text
        pygame.draw.rect(DISPLAYSURF, WHITE, (5, 5, 150, 75))
        pygame.draw.rect(DISPLAYSURF, BLACK, (5, 5, 150, 75), 2)
        
        DISPLAYSURF.blit(score_text, (10, 10))
        DISPLAYSURF.blit(coins_text, (10, 35))
        DISPLAYSURF.blit(speed_text, (10, 60))
    
    else:  # GAME_OVER state
        show_game_over(SCORE, COINS_COLLECTED)
    
    pygame.display.update()
    FramePerSec.tick(FPS)