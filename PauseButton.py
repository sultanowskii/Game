import pygame
from Button import Button


class PauseButton(Button):
    def __init__(self, x, y, sprite, group, size_x, size_y):
        super().__init__(group, x, y, size_x, size_y)
        self.on_sprite = sprite
        self.off_sprite = sprite
        self.image = sprite
        self.rect = self.image.get_rect().move(x, y)
        self.n = size_x
        self.m = size_y

    def isMouseOn(self, pos):
        return super().isMouseOn(pos)