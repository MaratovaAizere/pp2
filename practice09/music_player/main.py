import pygame
import sys
import os
from player import MusicPlayer


def main():
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")

    font = pygame.font.SysFont(None, 36)

    BASE_DIR = os.path.dirname(__file__)
    music_path = os.path.join(BASE_DIR, "music")

    player = MusicPlayer(music_path)

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()

                elif event.key == pygame.K_s:
                    player.stop()

                elif event.key == pygame.K_n:
                    player.next_track()

                elif event.key == pygame.K_b:
                    player.prev_track()

                elif event.key == pygame.K_q:
                    running = False

        track_name = player.get_current_track_name()
        text = font.render(f"Track: {track_name}", True, (255, 255, 255))
        screen.blit(text, (50, 100))

        if player.is_playing:
            status = "Playing"
            color = (0, 200, 0)
        else:
            status = "Stopped"
            color = (200, 0, 0)

        status_text = font.render(f"Status: {status}", True, color)
        screen.blit(status_text, (50, 150))

        controls1 = font.render("P - Play", True, (180, 180, 180))
        controls2 = font.render("S - Stop", True, (180, 180, 180))
        controls3 = font.render("N - Next", True, (180, 180, 180))
        controls4 = font.render("B - Previous", True, (180, 180, 180))
        controls5 = font.render("Q - Quit", True, (180, 180, 180))

        screen.blit(controls1, (50, 200))
        screen.blit(controls2, (50, 235))
        screen.blit(controls3, (50, 270))
        screen.blit(controls4, (50, 305))
        screen.blit(controls5, (50, 340))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()