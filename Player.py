import pygame
from AnimatedSprite import AnimatedSprite


class Player(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, group):  # think about making a mask here
        super().__init__(sheet, columns, rows, x, y, group)

    def move_up(self, speed):
        self.rect.y -= speed

    def move_down(self, speed):
        self.rect.y += speed

    def move_right(self, speed):
        self.rect.x += speed

    def move_left(self, speed):
        self.rect.x -= speed

    def cut_sheet(self, sheet, columns, rows):
        super().cut_sheet(sheet, columns, rows)

    def update(self):
        pass
