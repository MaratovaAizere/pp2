import pygame          # библиотека для графики и окна
import datetime        # текущее время
import math            # sin, cos, radians
import os              # работа с путями к файлам
import sys             # завершение программы

pygame.init()          # запуск модулей pygame

W, H = 600, 400
CENTER = (W // 2, H // 2)   # центр окна

screen = pygame.display.set_mode((W, H))   # создать окно
pygame.display.set_caption("Mickey Clock") # название окна

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (239, 228, 176)
DARK = (30, 30, 30)

clock = pygame.time.Clock()  # контроль FPS

base = os.path.dirname(__file__)          # папка текущего файла
img_path = os.path.join(base, "images")   # путь к папке images

face = pygame.image.load(os.path.join(img_path, "mickey.png")).convert_alpha()
face = pygame.transform.scale(face, (W, H))  # подгоняем картинку под окно

def get_hand_end(center, angle_deg, length):
    angle_rad = math.radians(angle_deg - 90)  # перевод в радианы, 0° вверх
    x = center[0] + length * math.cos(angle_rad)
    y = center[1] + length * math.sin(angle_rad)
    return int(x), int(y)

def draw_hand(surface, color, center, angle, length, width):
    end_pos = get_hand_end(center, angle, length)  # конец стрелки
    pygame.draw.line(surface, color, center, end_pos, width)  # рисуем линию

def get_angles(now):
    h = now.hour % 12
    m = now.minute
    s = now.second + now.microsecond / 1_000_000

    hour_angle = h * 30 + m * 0.5     # часовая
    minute_angle = m * 6 + s * 0.1    # минутная
    second_angle = s * 6              # секундная

    return hour_angle, minute_angle, second_angle

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = datetime.datetime.now()  # текущее время

    hour_angle, minute_angle, second_angle = get_angles(now)

    screen.fill(WHITE)         # очистка экрана
    screen.blit(face, (0, 0))  # рисуем фон

    draw_hand(screen, BLACK, CENTER, hour_angle, 70, 6)   # часовая
    draw_hand(screen, DARK, CENTER, minute_angle, 100, 4) # минутная
    draw_hand(screen, RED, CENTER, second_angle, 120, 2)  # секундная

    pygame.draw.circle(screen, BLACK, CENTER, 6)  # центр часов

    pygame.display.flip()  # показать кадр
    clock.tick(60)         # 60 FPS

pygame.quit()  # корректно закрыть pygame
sys.exit()     # завершить программу