import pygame
import sys
import os
from clock import MickeyClock


def main():
    pygame.init()

    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    clock = pygame.time.Clock()

    BASE_DIR = os.path.dirname(__file__)

    mickey_img = pygame.image.load(os.path.join(BASE_DIR, "images", "mickey.png")).convert_alpha()
    right_hand = pygame.image.load(os.path.join(BASE_DIR, "images", "right_hand.png")).convert_alpha()
    left_hand = pygame.image.load(os.path.join(BASE_DIR, "images", "left_hand.png")).convert_alpha()

    mickey_img = pygame.transform.scale(mickey_img, (600, 600))
    right_hand = pygame.transform.scale(right_hand, (490, 490))
    left_hand = pygame.transform.scale(left_hand, (490, 490))

    center = (WIDTH // 2, HEIGHT // 2)

    mickey_clock = MickeyClock(screen, center, mickey_img, right_hand, left_hand)

    running = True
    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mickey_clock.draw()

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()