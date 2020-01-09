import pygame
from AnimatedSprite import AnimatedSprite


class Enemy(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, group):  # think about making a mask here
        super().__init__(sheet, columns, rows, x, y, group)

    def cut_sheet(self, sheet, columns, rows):
        super().cut_sheet(sheet, columns, rows)

    def update(self):
        pass  # анимация и т.д.
