import pygame
import datetime
import math
import os
import sys

pygame.init()

W, H = 600, 400
CENTER = (W // 2, H // 2)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mickey Clock")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (239, 228, 176)
DARK = (30, 30, 30)

font = pygame.font.SysFont("Arial", 28, bold=True)
clock = pygame.time.Clock()

base = os.path.dirname(__file__)
img_path = os.path.join(base, "images")

face = pygame.image.load(os.path.join(img_path, "mickey.png")).convert_alpha()
face = pygame.transform.scale(face, (W, H))

def get_hand_end(center, angle_deg, length):
    angle_rad = math.radians(angle_deg - 90)
    x = center[0] + length * math.cos(angle_rad)
    y = center[1] + length * math.sin(angle_rad)
    return int(x), int(y)

def draw_hand(surface, color, center, angle, length, width):
    end_pos = get_hand_end(center, angle, length)
    pygame.draw.line(surface, color, center, end_pos, width)

def get_angles(now):
    h = now.hour % 12
    m = now.minute
    s = now.second + now.microsecond / 1_000_000

    hour_angle = h * 30 + m * 0.5
    minute_angle = m * 6 + s * 0.1
    second_angle = s * 6

    return hour_angle, minute_angle, second_angle


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = datetime.datetime.now()

    hour_angle, minute_angle, second_angle = get_angles(now)

    screen.fill(WHITE)
    screen.blit(face, (0, 0))

    draw_hand(screen, BLACK, CENTER, hour_angle, 70, 6)
    draw_hand(screen, DARK, CENTER, minute_angle, 100, 4)
    draw_hand(screen, RED, CENTER, second_angle, 120, 2)

    pygame.draw.circle(screen, BLACK, CENTER, 6)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()