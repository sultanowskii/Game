import pygame
from AnimatedSprite import AnimatedSprite


class Player(AnimatedSprite):
    def __init__(self, width, height, pos_x, pos_y, group):
        super().__init__(group)

    def move_up(self, speed):
        self.rect.move(-speed, 0)

    def move_down(self, speed):
        self.rect.move(speed, 0)

    def move_right(self, speed):
        self.rect.move(0, speed)

    def move_left(self, speed):
        self.rect.move(0, -speed)

    def cut_sheet(self, sheet, columns, rows):
        super().cut_sheet(sheet, columns, rows)

    def update(self):
        pass    # анимация и т.д.