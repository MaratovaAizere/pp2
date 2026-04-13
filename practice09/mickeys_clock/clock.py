import pygame
from datetime import datetime


class MickeyClock:
    def __init__(self, screen, center, mickey_img, right_hand, left_hand):
        self.screen = screen
        self.center = center
        self.mickey_img = mickey_img
        self.right_hand = right_hand
        self.left_hand = left_hand

    def get_time(self):
        now = datetime.now()
        return now.minute, now.second

    def get_angles(self, minutes, seconds):
        minute_angle = minutes * 6
        second_angle = seconds * 6
        return minute_angle, second_angle

    def draw_hand(self, image, angle, offset):
        rotated = pygame.transform.rotate(image, -angle)

        new_rect = rotated.get_rect(center=(
            self.center[0] + offset[0],
            self.center[1] + offset[1]
        ))

        self.screen.blit(rotated, new_rect)

    def draw(self):
        self.screen.blit(self.mickey_img, (0, 0))

        minutes, seconds = self.get_time()
        minute_angle, second_angle = self.get_angles(minutes, seconds)

        self.draw_hand(self.right_hand, second_angle, (0, 0))
        self.draw_hand(self.left_hand, minute_angle, (0, 0))