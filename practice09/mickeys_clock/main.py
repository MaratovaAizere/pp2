import pygame
from clock import MickeyClock


def main():
    pygame.init()

    app = MickeyClock()
    app.run()

    pygame.quit()


if __name__ == "__main__":
    main()